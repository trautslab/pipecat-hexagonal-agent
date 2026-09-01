# 🎯 Caso de Uso: UC-003 - Conmutación Cloud e Híbrida

- **ID:** `UC-003`
- **Dominio:** Cloud AI / Scalability
- **Actor Principal:** Ingeniero de DevOps / Administrador
- **Estado:** `APPROVED`

---

## 📖 Descripción
El sistema conmuta dinámicamente entre adaptadores locales y adaptadores cloud (Deepgram, OpenAI GPT-4o, Cartesia, Daily WebRTC) para soportar despliegues de alta concurrencia o salas WebRTC multiplataforma, únicamente cambiando valores en el archivo `.env`.
