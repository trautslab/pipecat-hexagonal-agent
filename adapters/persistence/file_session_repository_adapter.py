import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from config.logger_config import logger
from core.ports.session_repository_port import SessionRepositoryPort

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SESSIONS_DIR = PROJECT_ROOT / ".agents" / "sessions"


class FileSessionRepositoryAdapter(SessionRepositoryPort):
    """
    Adaptador de persistencia basado en archivos JSON en el sistema de archivos del servidor.
    Almacena cada sesión en .agents/sessions/<session_id>.json de forma agnóstica a navegadores.
    """

    def __init__(self, storage_dir: Path = SESSIONS_DIR):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, session_id: str) -> Path:
        safe_id = "".join(c for c in session_id if c.isalnum() or c in "_-")
        return self.storage_dir / f"{safe_id}.json"

    def list_sessions(self) -> List[Dict[str, Any]]:
        sessions = []
        try:
            for file in sorted(self.storage_dir.glob("*.json"), key=os.path.getmtime, reverse=True):
                try:
                    data = json.loads(file.read_text(encoding="utf-8"))
                    sessions.append(data)
                except Exception as e:
                    logger.warning(f"Error leyendo sesión {file}: {e}")
        except Exception as e:
            logger.warning(f"Error listando sesiones: {e}")
        return sessions

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        path = self._get_path(session_id)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning(f"Error cargando sesión {session_id}: {e}")
            return None

    def save_session(self, session_data: Dict[str, Any]) -> bool:
        session_id = session_data.get("id")
        if not session_id:
            return False
        path = self._get_path(session_id)
        try:
            path.write_text(json.dumps(session_data, indent=2, ensure_ascii=False), encoding="utf-8")
            return True
        except Exception as e:
            logger.warning(f"Error guardando sesión {session_id}: {e}")
            return False

    def append_console_step(self, session_id: str, turn_index: int, step: Dict[str, Any]) -> bool:
        session = self.get_session(session_id)
        if not session:
            session = {
                "id": session_id,
                "title": "Nueva Conversación",
                "createdAt": os.environ.get("TIMESTAMP", ""),
                "turnCounter": turn_index,
                "messages": [],
                "consoleLogs": []
            }
        
        if "consoleLogs" not in session:
            session["consoleLogs"] = []
        
        turn_entry = None
        for t in session["consoleLogs"]:
            if t.get("turnIndex") == turn_index:
                turn_entry = t
                break
        
        if not turn_entry:
            turn_entry = {
                "turnIndex": turn_index,
                "timestamp": step.get("timestamp", ""),
                "steps": [],
                "status": "processing"
            }
            session["consoleLogs"].append(turn_entry)
        
        turn_entry["steps"].append(step)
        return self.save_session(session)

    def delete_session(self, session_id: str) -> bool:
        path = self._get_path(session_id)
        if path.exists():
            try:
                path.unlink()
                logger.info(f"🗑️ [SessionRepository] Sesión {session_id} eliminada del servidor.")
                return True
            except Exception as e:
                logger.warning(f"Error eliminando sesión {session_id}: {e}")
                return False
        return False
