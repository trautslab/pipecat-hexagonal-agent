from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class ConversationMessage:
    role: str
    content: str
    timestamp: datetime = field(default_factory=get_utc_now)


@dataclass
class AgentSession:
    """
    Entidad de dominio que representa la sesión activa del agente de voz.
    Mantiene el estado y el historial independiente de los servicios de IA.
    """
    session_id: str
    agent_name: str
    language: str
    system_prompt: str
    created_at: datetime = field(default_factory=get_utc_now)
    messages: List[ConversationMessage] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_user_message(self, text: str):
        self.messages.append(ConversationMessage(role="user", content=text))

    def add_assistant_message(self, text: str):
        self.messages.append(ConversationMessage(role="assistant", content=text))

    def get_context_for_llm(self) -> List[Dict[str, str]]:
        context = [{"role": "system", "content": self.system_prompt}]
        for msg in self.messages:
            context.append({"role": msg.role, "content": msg.content})
        return context
