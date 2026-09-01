import asyncio
import os
import sys
import json
import base64
import hashlib
import struct
from pathlib import Path
from config.logger_config import logger
from config.settings import settings, TransportProviderType, AppSettings
from factories.agent_factory import AgentFactory

WEB_DIR = Path(__file__).resolve().parent / "web"
WS_MAGIC_STRING = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


class PurePythonWebSocket:
    """Implementación ligera de RFC 6455 WebSocket para streaming de audio binario y texto."""
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.closed = False

    async def send_str(self, text: str):
        if self.closed:
            return
        payload = text.encode("utf-8")
        header = bytearray([0x81]) # Fin=1, Opcode=1 (Text)
        length = len(payload)
        if length <= 125:
            header.append(length)
        elif length <= 65535:
            header.append(126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(127)
            header.extend(struct.pack("!Q", length))
        try:
            self.writer.write(header + payload)
            await self.writer.drain()
        except Exception:
            self.closed = True

    async def send_bytes(self, data: bytes):
        if self.closed:
            return
        header = bytearray([0x82]) # Fin=1, Opcode=2 (Binary)
        length = len(data)
        if length <= 125:
            header.append(length)
        elif length <= 65535:
            header.append(126)
            header.extend(struct.pack("!H", length))
        else:
            header.append(127)
            header.extend(struct.pack("!Q", length))
        try:
            self.writer.write(header + data)
            await self.writer.drain()
        except Exception:
            self.closed = True

    async def receive(self) -> Optional[bytes]:
        """Lee y desenmascara una trama del cliente web."""
        try:
            head = await self.reader.readexactly(2)
            b1, b2 = head[0], head[1]
            opcode = b1 & 0x0F
            masked = (b2 & 0x80) != 0
            payload_len = b2 & 0x7F

            if opcode == 0x8: # Close frame
                self.closed = True
                return None

            if payload_len == 126:
                ext = await self.reader.readexactly(2)
                payload_len = struct.unpack("!H", ext)[0]
            elif payload_len == 127:
                ext = await self.reader.readexactly(8)
                payload_len = struct.unpack("!Q", ext)[0]

            masks = await self.reader.readexactly(4) if masked else None
            data = await self.reader.readexactly(payload_len)

            if masked:
                unmasked = bytearray(data)
                for i in range(len(data)):
                    unmasked[i] ^= masks[i % 4]
                return bytes(unmasked)
            return data
        except Exception:
            self.closed = True
            return None


async def handle_static_request(reader, writer, path):
    """Sirve archivos estáticos (HTML, CSS, JS) con caché y MIME types correctos."""
    clean_path = path.split("?")[0]
    if clean_path == "/" or clean_path == "":
        file_path = WEB_DIR / "index.html"
    else:
        file_path = WEB_DIR / clean_path.lstrip("/")

    if file_path.exists() and file_path.is_file():
        content_type = "text/html"
        if file_path.suffix == ".css":
            content_type = "text/css"
        elif file_path.suffix == ".js":
            content_type = "application/javascript"
        elif file_path.suffix == ".json":
            content_type = "application/json"
        elif file_path.suffix == ".svg":
            content_type = "image/svg+xml"

        content = file_path.read_bytes()
        header = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: {content_type}; charset=utf-8\r\n"
            f"Content-Length: {len(content)}\r\n"
            f"Access-Control-Allow-Origin: *\r\n"
            f"Connection: close\r\n\r\n"
        )
        writer.write(header.encode() + content)
    else:
        not_found = b"HTTP/1.1 404 Not Found\r\nContent-Length: 9\r\n\r\nNot Found"
        writer.write(not_found)
    await writer.drain()
    writer.close()


async def handle_client_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """Maneja tanto peticiones HTTP como Upgrades de WebSocket en el mismo puerto."""
    try:
        request_line = await reader.readline()
        if not request_line:
            writer.close()
            return

        parts = request_line.decode().strip().split()
        if len(parts) < 2:
            writer.close()
            return

        method, path = parts[0], parts[1]
        headers = {}

        # Leer cabeceras HTTP
        while True:
            line = await reader.readline()
            if not line or line == b"\r\n":
                break
            line_str = line.decode().strip()
            if ":" in line_str:
                k, v = line_str.split(":", 1)
                headers[k.strip().lower()] = v.strip()

        # Comprobar si es un Upgrade a WebSocket
        if headers.get("upgrade", "").lower() == "websocket" and "sec-websocket-key" in headers:
            key = headers["sec-websocket-key"]
            accept_hash = hashlib.sha1(key.encode("utf-8") + WS_MAGIC_STRING).digest()
            accept_key = base64.b64encode(accept_hash).decode("utf-8")

            upgrade_response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
            )
            writer.write(upgrade_response.encode())
            await writer.drain()

            logger.info("🔗 [WebSocket] Cliente conectado exitosamente desde el navegador.")
            ws = PurePythonWebSocket(reader, writer)
            await run_agent_websocket_session(ws)
        else:
            await handle_static_request(reader, writer, path)
    except Exception as e:
        logger.warning(f"Error procesando conexión: {e}")
        try:
            writer.close()
        except Exception:
            pass


async def run_agent_websocket_session(ws: PurePythonWebSocket):
    """Orquesta la sesión conversacional del agente con el cliente WebSocket."""
    # 1. Enviar estado inicial al navegador
    await ws.send_str(json.dumps({
        "type": "status",
        "state": "connected",
        "agent": settings.agent_name,
        "stt": settings.stt_provider.value,
        "llm": settings.llm_provider.value,
        "tts": settings.tts_provider.value
    }))

    # 2. Configurar agente con WebSocketTransportAdapter
    config = AppSettings(
        TRANSPORT_PROVIDER=TransportProviderType.WEBSOCKET,
        AGENT_NAME=settings.agent_name,
        AGENT_SYSTEM_PROMPT=settings.agent_system_prompt
    )
    agent = AgentFactory.build_agent(config)
    transport_adapter = agent.transport
    transport_adapter.attach_websocket(ws)

    # 3. Enviar saludo de bienvenida
    await ws.send_str(json.dumps({
        "type": "caption",
        "role": "bot",
        "text": "¡Hola! Estoy conectado y listo. ¿De qué te gustaría hablar hoy?"
    }))

    # 4. Bucle de recepción de audio del cliente
    try:
        while not ws.closed:
            chunk = await ws.receive()
            if chunk is None:
                break
            
            # Si el chunk es JSON (mensajes de control)
            if chunk.startswith(b"{") and chunk.endswith(b"}"):
                try:
                    msg = json.loads(chunk.decode("utf-8"))
                    if msg.get("action") == "ping":
                        await ws.send_str(json.dumps({"type": "pong"}))
                except Exception:
                    pass
            else:
                # Chunk de audio PCM binario
                await transport_adapter.handle_incoming_bytes(chunk)
    except Exception as e:
        logger.warning(f"Sesión WebSocket cerrada con aviso: {e}")
    finally:
        logger.info("🔌 [WebSocket] Cliente desconectado.")


async def start_web_server(host="0.0.0.0", port=8765):
    logger.info("=" * 60)
    logger.info(f"🌐 SERVIDOR WEB & WEBSOCKET EN VIVO")
    logger.info(f"👉 URL: http://localhost:{port}")
    logger.info(f"📁 Raíz estática: {WEB_DIR}")
    logger.info("=" * 60)
    server = await asyncio.start_server(handle_client_connection, host, port)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(start_web_server(port=settings.web_port))
    except KeyboardInterrupt:
        logger.info("\nServidor web detenido por el usuario.")
