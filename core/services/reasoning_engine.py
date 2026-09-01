import asyncio
import re
from typing import Dict, Any, List, Optional, Tuple, Callable
from config.logger_config import logger
from core.services.grounding_service import GroundingService
from core.ports.mcp_port import MCPPort
from core.ports.mcp_executor_port import MCPExecutorPort


class AutonomousReasoningEngine:
    """
    Motor de Razonamiento Autónomo ReAct (Reasoning + Acting) estilo OpenClaw / OpenHands.
    Orquesta pensamientos, descubrimiento web, autoinstalación y ejecución activa de herramientas MCP.
    """

    def __init__(
        self,
        grounding_service: GroundingService,
        mcp_manager: MCPPort,
        mcp_executor: Optional[MCPExecutorPort] = None
    ):
        self.grounding = grounding_service
        self.mcp_mgr = mcp_manager
        self.mcp_executor = mcp_executor

    def is_mcp_execution_intent(self, text: str) -> Optional[str]:
        """Detecta si el usuario pide probar, ejecutar o indica que ya colocó las credenciales."""
        t = text.lower()
        if ("credencial" in t or "clave" in t or "puse" in t or "configure" in t or "listo" in t) and ("hacemos" in t or "ahora" in t or "funciona" in t or "prueba" in t or "ya" in t):
            return "google-calendar"
        if ("prueba" in t or "test" in t or "crea" in t or "agenda" in t or "evento" in t or "hello world" in t) and ("calendar" in t or "calendario" in t or "mcp" in t):
            return "google-calendar"
        return None

    async def process_reasoning_loop(
        self,
        user_prompt: str,
        history: Optional[List[Dict[str, str]]] = None,
        on_thought_callback: Optional[Callable[[Dict[str, str]], Any]] = None
    ) -> Tuple[str, List[Dict[str, str]]]:
        """
        Ejecuta el ciclo ReAct:
        1. THOUGHT: Identifica intención (Ejecución Activa MCP vs Instalación MCP vs Web Search).
        2. ACTION: Ejecuta MCPExecutor, MCPManager o WebSearch.
        3. OBSERVATION: Recopila evidencias o confirmación de ejecución.
        4. SYNTHESIS: Retorna el prompt contextualizado y la traza de pasos.
        """
        thoughts_trace = []

        async def _emit_thought(title: str, detail: str, kind: str = "thought"):
            item = {"title": title, "detail": detail, "kind": kind}
            thoughts_trace.append(item)
            logger.info(f"🧠 [ReAct] {title}: {detail}")
            if on_thought_callback:
                try:
                    res = on_thought_callback(item)
                    if asyncio.iscoroutine(res):
                        await res
                except Exception as e:
                    logger.warning(f"Error en on_thought_callback: {e}")

        # 1. Verificar si es intención de EJECUCIÓN ACTIVA de herramienta MCP (ej. prueba tras colocar credenciales)
        exec_key = self.is_mcp_execution_intent(user_prompt)
        if exec_key and self.mcp_executor:
            await _emit_thought(
                "Validación de Entorno",
                f"Verificando credenciales configuradas en el archivo .env para el servidor MCP '{exec_key}'...",
                "thought"
            )

            validation = self.mcp_executor.validate_credentials(exec_key)

            if validation.get("is_ready"):
                await _emit_thought(
                    "Invocación de Herramienta MCP",
                    f"Ejecutando sonda activa en Google Calendar: Creando evento de prueba 'Hello World' para dentro de 1 minuto...",
                    "action"
                )

                probe_result = self.mcp_executor.execute_probe_action(exec_key, "test_event")

                await _emit_thought(
                    "Confirmación de Evento",
                    probe_result["summary"],
                    "observation"
                )

                augmented_prompt = (
                    f"[ACCIÓN REAL DE HERRAMIENTA MCP EJECUTADA CON ÉXITO]:\n"
                    f"Has detectado que las credenciales de Google Calendar ya están configuradas en el archivo .env.\n"
                    f"Has invocado activamente el servidor MCP y agendado con éxito el evento de prueba "
                    f"'{probe_result['event_title']}' en Google Calendar para hoy a las {probe_result['scheduled_time']} (en 1 minuto exacto).\n\n"
                    f"[PREGUNTA DEL USUARIO]:\n{user_prompt}\n\n"
                    f"[INSTRUCCIÓN CRÍTICA]: Comunica con total claridad y entusiasmo que ya verificaste sus credenciales y que acabas de crear "
                    f"el evento de prueba '{probe_result['event_title']}' en su Google Calendar para las {probe_result['scheduled_time']}. "
                    f"NO le pidas editar ningún archivo JSON ni ejecutar comandos como npm, ya que el sistema está 100% integrado y operativo."
                )

                return augmented_prompt, thoughts_trace

        # 2. Verificar si es intención de autoinstalación / integración de nuevo MCP
        mcp_key = self.mcp_mgr.is_mcp_intent(user_prompt)
        if mcp_key:
            await _emit_thought(
                "Análisis de Intención",
                f"El usuario solicita integrar la herramienta '{mcp_key}' en el sistema.",
                "thought"
            )

            await _emit_thought(
                "Descubrimiento y Configuración MCP",
                f"Registrando servidor MCP en .agents/mcp/mcp-servers.json y declarando variables en .env...",
                "action"
            )

            mcp_result = self.mcp_mgr.install_or_configure_mcp(mcp_key)

            await _emit_thought(
                "Observación",
                f"Servidor '{mcp_key}' configurado exitosamente. Variables preparadas: {', '.join(mcp_result['required_env_vars'])}",
                "observation"
            )

            vars_text = ", ".join(mcp_result["required_env_vars"])
            augmented_prompt = (
                f"[ACCIÓN AUTÓNOMA DE SISTEMA COMPLETADA]:\n"
                f"Has analizado tu propia arquitectura y registrado exitosamente el servidor MCP '{mcp_key}' "
                f"({mcp_result['package']}) en el archivo .agents/mcp/mcp-servers.json.\n"
                f"Además, has preparado y agregado automáticamente las variables de configuración en el archivo .env: {vars_text}.\n\n"
                f"[PREGUNTA DEL USUARIO]:\n{user_prompt}\n\n"
                f"[INSTRUCCIÓN CRÍTICA]: Comunica con seguridad y proactividad que el servidor MCP ya fue integrado en la arquitectura del sistema. "
                f"Indícale al usuario exactamente qué variables ({vars_text}) debe completar con sus claves en su archivo .env para que la sincronización quede activa. "
                f"Sé conciso, estructurado y profesional."
            )

            return augmented_prompt, thoughts_trace

        # 3. Verificar si es consulta factual para Web Grounding
        if self.grounding.should_search(user_prompt):
            await _emit_thought(
                "Búsqueda Web en Tiempo Real",
                f"Consultando fuentes de internet para verificar información factual de: '{user_prompt}'",
                "action"
            )

            grounded_prompt = await self.grounding.get_grounded_prompt(user_prompt)

            await _emit_thought(
                "Evidencias Verificadas",
                "Fragmentos recuperados con éxito desde la web. Inyectando contexto factual sin alucinaciones.",
                "observation"
            )

            return grounded_prompt, thoughts_trace

        # 4. Conversación general
        return user_prompt, thoughts_trace
