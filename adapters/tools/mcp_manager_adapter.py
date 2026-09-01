import json
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from config.logger_config import logger
from core.ports.mcp_port import MCPPort

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MCP_CONFIG_PATH = PROJECT_ROOT / ".agents" / "mcp" / "mcp-servers.json"
ENV_PATH = PROJECT_ROOT / ".env"
ENV_EXAMPLE_PATH = PROJECT_ROOT / ".env.example"


# Catálogo curado de paquetes MCP oficiales y comunes
KNOWN_MCP_SERVERS = {
    "google-calendar": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-google-calendar"],
        "env_vars": {
            "GOOGLE_CALENDAR_CLIENT_ID": "",
            "GOOGLE_CALENDAR_CLIENT_SECRET": "",
            "GOOGLE_CALENDAR_REDIRECT_URI": "http://localhost:8765/oauth2callback"
        },
        "description": "Servidor oficial de Google Calendar para crear, consultar y gestionar eventos y calendarios."
    },
    "postgres": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-postgres"],
        "env_vars": {
            "POSTGRES_CONNECTION_STRING": "postgresql://user:password@localhost:5432/mydb"
        },
        "description": "Servidor MCP para introspección y ejecución de consultas SQL en PostgreSQL."
    },
    "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env_vars": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": ""
        },
        "description": "Servidor oficial de GitHub para crear repositorios, issues y PRs."
    },
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", str(PROJECT_ROOT)],
        "env_vars": {},
        "description": "Servidor oficial para lectura y escritura segura en el sistema de archivos local."
    }
}


class MCPManagerAdapter(MCPPort):
    """
    Adaptador para la gestión dinámica e instalación de Servidores MCP (Model Context Protocol).
    Actualiza .agents/mcp/mcp-servers.json y declara credenciales en .env.
    """

    def __init__(self, mcp_file: Path = MCP_CONFIG_PATH, env_file: Path = ENV_PATH):
        self.mcp_file = mcp_file
        self.env_file = env_file

    def get_installed_servers(self) -> Dict[str, Any]:
        if not self.mcp_file.exists():
            return {}
        try:
            return json.loads(self.mcp_file.read_text(encoding="utf-8")).get("mcpServers", {})
        except Exception:
            return {}

    def is_mcp_intent(self, text: str) -> Optional[str]:
        """Detecta si la consulta del usuario solicita instalar o usar una herramienta MCP."""
        t = text.lower()
        if "google calendar" in t or "calendario de google" in t or "calendar" in t:
            return "google-calendar"
        if "postgres" in t or "postgresql" in t or "base de datos" in t:
            return "postgres"
        if "github" in t or "repositorio" in t:
            return "github"
        if "filesystem" in t or "archivos locales" in t:
            return "filesystem"
        
        # Detección genérica de "instalar mcp", "conectar mcp", "instalarte herramienta"
        if "mcp" in t and ("instala" in t or "conecta" in t or "configura" in t or "agrega" in t):
            match = re.search(r"(?:instala|conecta|configura|agrega)\s+(?:el\s+mcp\s+de\s+|mcp\s+)?([a-zA-Z0-9_-]+)", t)
            if match:
                return match.group(1).lower()
        return None

    def install_or_configure_mcp(self, server_key: str) -> Dict[str, Any]:
        """Registra el MCP en mcp-servers.json y declara las variables en .env."""
        logger.info(f"⚙️ [MCPManager] Configurando servidor MCP: '{server_key}'...")

        info = KNOWN_MCP_SERVERS.get(server_key)
        if not info:
            info = {
                "command": "npx",
                "args": ["-y", f"mcp-server-{server_key}"],
                "env_vars": {f"{server_key.upper().replace('-', '_')}_API_KEY": ""},
                "description": f"Servidor MCP dinámico para {server_key}."
            }

        # 1. Leer o inicializar mcp-servers.json
        self.mcp_file.parent.mkdir(parents=True, exist_ok=True)
        config = {"mcpServers": {}}
        if self.mcp_file.exists():
            try:
                config = json.loads(self.mcp_file.read_text(encoding="utf-8"))
            except Exception:
                config = {"mcpServers": {}}

        if "mcpServers" not in config:
            config["mcpServers"] = {}

        env_mapping = {}
        for var_name in info["env_vars"]:
            env_mapping[var_name] = f"${{{var_name}}}"

        config["mcpServers"][server_key] = {
            "command": info["command"],
            "args": info["args"],
            "env": env_mapping,
            "description": info["description"]
        }

        self.mcp_file.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info(f"✅ [MCPManager] .agents/mcp/mcp-servers.json actualizado con '{server_key}'.")

        # 2. Agregar claves al archivo .env si no existen
        env_content = ""
        if self.env_file.exists():
            env_content = self.env_file.read_text(encoding="utf-8")
        elif ENV_EXAMPLE_PATH.exists():
            env_content = ENV_EXAMPLE_PATH.read_text(encoding="utf-8")

        missing_vars = []
        appended_lines = []

        for var_name, default_val in info["env_vars"].items():
            if var_name not in env_content:
                missing_vars.append(var_name)
                appended_lines.append(f"\n# Credenciales requeridas para MCP: {server_key}\n{var_name}={default_val}\n")

        if appended_lines:
            with open(self.env_file, "a", encoding="utf-8") as f:
                f.write("".join(appended_lines))
            logger.info(f"✅ [MCPManager] Declaradas variables {missing_vars} en .env.")

        return {
            "status": "success",
            "server_key": server_key,
            "package": " ".join([info["command"]] + info["args"]),
            "required_env_vars": list(info["env_vars"].keys()),
            "missing_env_vars": missing_vars,
            "description": info["description"]
        }
