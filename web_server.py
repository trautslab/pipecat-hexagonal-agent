import asyncio
import os
import sys
from pathlib import Path
from config.logger_config import logger
from config.settings import settings, TransportProviderType, AppSettings
from factories.agent_factory import AgentFactory

WEB_DIR = Path(__file__).resolve().parent / "web"


async def handle_static_request(reader, writer, path):
    """Sirve archivos estáticos (HTML, CSS, JS) sin frameworks pesados."""
    if path == "/" or path == "":
        file_path = WEB_DIR / "index.html"
    else:
        file_path = WEB_DIR / path.lstrip("/")

    if file_path.exists() and file_path.is_file():
        content_type = "text/html"
        if file_path.suffix == ".css":
            content_type = "text/css"
        elif file_path.suffix == ".js":
            content_type = "application/javascript"
        elif file_path.suffix == ".json":
            content_type = "application/json"

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


async def handle_http_connection(reader, writer):
    try:
        line = await reader.readline()
        if not line:
            writer.close()
            return
        request_line = line.decode().strip()
        parts = request_line.split()
        if len(parts) >= 2:
            method, path = parts[0], parts[1]
            await handle_static_request(reader, writer, path)
        else:
            writer.close()
    except Exception as e:
        logger.warning(f"Error HTTP request: {e}")
        writer.close()


async def start_web_server(host="0.0.0.0", port=8765):
    logger.info(f"🌐 Servidor Web iniciado en http://localhost:{port}")
    logger.info(f"📁 Sirviendo frontend desde: {WEB_DIR}")
    server = await asyncio.start_server(handle_http_connection, host, port)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(start_web_server(port=settings.web_port))
    except KeyboardInterrupt:
        logger.info("Servidor web detenido.")
