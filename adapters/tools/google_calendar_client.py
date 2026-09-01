import os
import json
import urllib.request
import urllib.parse
import urllib.error
import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from config.logger_config import logger

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
TOKENS_DIR = PROJECT_ROOT / ".agents" / "tokens"
TOKEN_FILE = TOKENS_DIR / "google_token.json"


class GoogleCalendarClient:
    """
    Cliente nativo para Google OAuth2 y Google Calendar API v3 (googleapis.com).
    Ejecuta llamadas REST reales para autenticación e inserción de eventos.
    """

    def __init__(self, env_file: Path = ENV_PATH, token_file: Path = TOKEN_FILE):
        self.env_file = env_file
        self.token_file = token_file
        self.token_file.parent.mkdir(parents=True, exist_ok=True)

    def _get_credentials_from_env(self) -> Dict[str, str]:
        creds = {}
        if self.env_file.exists():
            for line in self.env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    creds[k.strip()] = v.strip()
        return creds

    def get_auth_url(self) -> str:
        creds = self._get_credentials_from_env()
        client_id = creds.get("GOOGLE_CALENDAR_CLIENT_ID", "")
        redirect_uri = creds.get("GOOGLE_CALENDAR_REDIRECT_URI", "http://localhost:8765/oauth2callback")
        scope = "https://www.googleapis.com/auth/calendar.events"

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scope,
            "access_type": "offline",
            "prompt": "consent"
        }
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"

    def exchange_code(self, code: str) -> Dict[str, Any]:
        """Intercambia el código de autorización por access_token y refresh_token."""
        creds = self._get_credentials_from_env()
        client_id = creds.get("GOOGLE_CALENDAR_CLIENT_ID", "")
        client_secret = creds.get("GOOGLE_CALENDAR_CLIENT_SECRET", "")
        redirect_uri = creds.get("GOOGLE_CALENDAR_REDIRECT_URI", "http://localhost:8765/oauth2callback")

        token_url = "https://oauth2.googleapis.com/token"
        payload = urllib.parse.urlencode({
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }).encode("utf-8")

        req = urllib.request.Request(
            token_url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                
                # Calcular expiración
                expires_in = data.get("expires_in", 3600)
                data["expires_at"] = (datetime.datetime.now() + datetime.timedelta(seconds=expires_in)).isoformat()

                self.token_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
                logger.info(f"✅ [GoogleCalendarClient] Tokens guardados exitosamente en {self.token_file}.")
                return {"status": "success", "tokens": data}
        except Exception as e:
            logger.error(f"❌ [GoogleCalendarClient] Error intercambiando código OAuth2: {e}")
            return {"status": "error", "error": str(e)}

    def get_valid_access_token(self) -> Optional[str]:
        """Obtiene un token de acceso válido o lo refresca usando el refresh_token."""
        if not self.token_file.exists():
            return None

        try:
            token_data = json.loads(self.token_file.read_text(encoding="utf-8"))
            access_token = token_data.get("access_token")
            refresh_token = token_data.get("refresh_token")
            expires_at_str = token_data.get("expires_at")

            # Verificar si expiró
            is_expired = True
            if expires_at_str:
                try:
                    exp_dt = datetime.datetime.fromisoformat(expires_at_str)
                    if exp_dt > datetime.datetime.now():
                        is_expired = False
                except Exception:
                    is_expired = True

            if not is_expired and access_token:
                return access_token

            # Refrescar con refresh_token
            if refresh_token:
                creds = self._get_credentials_from_env()
                client_id = creds.get("GOOGLE_CALENDAR_CLIENT_ID", "")
                client_secret = creds.get("GOOGLE_CALENDAR_CLIENT_SECRET", "")

                token_url = "https://oauth2.googleapis.com/token"
                payload = urllib.parse.urlencode({
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                }).encode("utf-8")

                req = urllib.request.Request(
                    token_url,
                    data=payload,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )

                with urllib.request.urlopen(req, timeout=15) as resp:
                    new_data = json.loads(resp.read().decode("utf-8"))
                    token_data["access_token"] = new_data["access_token"]
                    expires_in = new_data.get("expires_in", 3600)
                    token_data["expires_at"] = (datetime.datetime.now() + datetime.timedelta(seconds=expires_in)).isoformat()
                    
                    self.token_file.write_text(json.dumps(token_data, indent=2), encoding="utf-8")
                    logger.info("🔄 [GoogleCalendarClient] Access token refrescado exitosamente.")
                    return token_data["access_token"]
            return access_token
        except Exception as e:
            logger.warning(f"Error verificando token de Google: {e}")
            return None

    def insert_real_event(
        self,
        title: str,
        target_time: Optional[str] = None,
        date: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        duration_minutes: int = 30
    ) -> Dict[str, Any]:
        """Inserta un evento real en Google Calendar API v3 con metadatos completos."""
        token = self.get_valid_access_token()
        
        if not token:
            auth_url = self.get_auth_url()
            logger.info("⚠️ [GoogleCalendarClient] Se requiere autorización previa del usuario.")
            return {
                "status": "auth_required",
                "auth_url": auth_url,
                "message": "Se requiere autorización de tu cuenta de Google. Haz clic en el enlace para conectar."
            }

        now = datetime.datetime.now()

        # 1. Parsear Fecha
        year, month, day = now.year, now.month, now.day
        if date:
            try:
                if "-" in date:
                    dp = date.split("-")
                    year, month, day = int(dp[0]), int(dp[1]), int(dp[2])
                elif "/" in date:
                    dp = date.split("/")
                    day, month, year = int(dp[0]), int(dp[1]), int(dp[2])
            except Exception as e:
                logger.warning(f"Error parseando fecha '{date}': {e}")

        # 2. Parsear Hora de Inicio
        h, m = now.hour, now.minute
        if target_time:
            try:
                clean_time = target_time.replace("p.m.", "").replace("a.m.", "").replace("pm", "").replace("am", "").strip()
                parts = clean_time.split(":")
                h = int(parts[0])
                m = int(parts[1]) if len(parts) > 1 else 0
                if ("p.m." in target_time.lower() or "pm" in target_time.lower() or "tarde" in target_time.lower() or "noche" in target_time.lower()) and h < 12:
                    h += 12
                start_dt = datetime.datetime(year, month, day, h, m, 0)
            except Exception as e:
                logger.warning(f"Error parseando hora '{target_time}': {e}")
                start_dt = datetime.datetime(year, month, day, h, m, 0) + datetime.timedelta(minutes=1)
        else:
            start_dt = datetime.datetime(year, month, day, h, m, 0) + datetime.timedelta(minutes=1)

        end_dt = start_dt + datetime.timedelta(minutes=duration_minutes)

        # Formatear ISO 8601 con offset de Lima (UTC-5)
        tz_offset = "-05:00"
        start_iso = start_dt.strftime("%Y-%m-%dT%H:%M:%S") + tz_offset
        end_iso = end_dt.strftime("%Y-%m-%dT%H:%M:%S") + tz_offset

        final_desc = description or (
            f"🎬 Recordatorio: {title}\n"
            f"📅 Fecha: {start_dt.strftime('%d/%m/%Y')} a las {start_dt.strftime('%H:%M')} hrs\n"
            f"✨ Agendado automáticamente por Aura Voice AI. ¡Que tengas un excelente día!"
        )

        event_payload = {
            "summary": title,
            "description": final_desc,
            "start": {
                "dateTime": start_iso,
                "timeZone": "America/Lima"
            },
            "end": {
                "dateTime": end_iso,
                "timeZone": "America/Lima"
            }
        }

        if location:
            event_payload["location"] = location

        api_url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
        data_bytes = json.dumps(event_payload).encode("utf-8")

        req = urllib.request.Request(
            api_url,
            data=data_bytes,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        try:
            logger.info(f"🌐 [GoogleCalendarClient] Enviando POST a {api_url}...")
            with urllib.request.urlopen(req, timeout=15) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                html_link = res_data.get("htmlLink", "https://calendar.google.com")
                event_id = res_data.get("id")

                logger.info(f"🎉 [GoogleCalendarClient] ¡EVENTO REAL CREADO EN GOOGLE CALENDAR! ID: {event_id}, Link: {html_link}")

                return {
                    "status": "success",
                    "server": "google-calendar",
                    "event_id": event_id,
                    "event_title": title,
                    "scheduled_time": start_dt.strftime("%H:%M:%S"),
                    "date": start_dt.strftime("%d/%m/%Y"),
                    "html_link": html_link,
                    "summary": f"Evento '{title}' creado físicamente en tu Google Calendar para hoy a las {start_dt.strftime('%H:%M:%S')}. Enlace directo: {html_link}"
                }
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            logger.error(f"❌ [GoogleCalendarClient] Error de Google API ({e.code}): {err_body}")
            if e.code == 401:
                return {
                    "status": "auth_required",
                    "auth_url": self.get_auth_url(),
                    "message": "Token de Google expirado o inválido. Por favor vuelve a autorizar la cuenta."
                }
            return {
                "status": "error",
                "error": f"Error de Google Calendar API: {err_body}"
            }
        except Exception as e:
            logger.error(f"❌ [GoogleCalendarClient] Error de conexión con Google APIs: {e}")
            return {"status": "error", "error": str(e)}
