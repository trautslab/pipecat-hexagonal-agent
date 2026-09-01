/**
 * Aura Voice AI - Web Client v0.5.0
 * Soporte para Historial de Conversaciones Persistente (ChatGPT/Claude UI),
 * Botón de Copiado Inteligente, AudioContext Canvas Visualizer y Streaming WebSocket.
 */

class VoiceAgentApp {
  constructor() {
    this.audioContext = null;
    this.mediaStream = null;
    this.audioInput = null;
    this.processor = null;
    this.analyser = null;
    this.recognition = null;
    this.socket = null;
    this.isConnected = false;
    this.isSpeaking = false;

    // Sessions & Chat State
    this.sessions = [];
    this.currentSessionId = null;

    // DOM Elements
    this.themeToggleBtn = document.getElementById("theme-toggle-btn");
    this.themeIcon = document.getElementById("theme-icon");
    this.toggleSidebarBtn = document.getElementById("toggle-sidebar-btn");
    this.sidebar = document.getElementById("sidebar");
    this.newChatBtn = document.getElementById("new-chat-btn");
    this.historyList = document.getElementById("history-list");
    this.currentChatTitle = document.getElementById("current-chat-title");

    this.toggleMicBtn = document.getElementById("toggle-mic-btn");
    this.btnText = document.getElementById("btn-text");
    this.statusBadge = document.getElementById("status-badge");
    this.statusText = document.getElementById("status-text");
    this.canvas = document.getElementById("waveform-canvas");
    this.canvasCtx = this.canvas.getContext("2d");
    this.stageOverlay = document.getElementById("stage-overlay");
    this.captionsStream = document.getElementById("captions-stream");
    this.audioTestBtn = document.getElementById("audio-test-btn");
    this.clearCaptionsBtn = document.getElementById("clear-captions-btn");

    this.animationId = null;
    this.dataArray = null;
    this.phase = 0;

    this.initTheme();
    this.initSessions();
    this.initEvents();
    this.resizeCanvas();
    this.startIdleAnimation();
  }

  /* ============================================================================
     1. THEME SWITCHER (Light / Dark Mode)
     ============================================================================ */
  initTheme() {
    const savedTheme = localStorage.getItem("aura-theme") || "dark";
    this.setTheme(savedTheme);

    this.themeToggleBtn.addEventListener("click", () => {
      const currentTheme = document.documentElement.getAttribute("data-theme") || "dark";
      const nextTheme = currentTheme === "dark" ? "light" : "dark";
      this.setTheme(nextTheme);
    });
  }

  setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("aura-theme", theme);
    this.themeIcon.textContent = theme === "dark" ? "🌙" : "☀️";
  }

  /* ============================================================================
     2. SESSIONS & CHAT PERSISTENCE (ChatGPT / Claude Style)
     ============================================================================ */
  initSessions() {
    const rawSessions = localStorage.getItem("aura_conversations");
    if (rawSessions) {
      try {
        this.sessions = JSON.parse(rawSessions);
      } catch (e) {
        this.sessions = [];
      }
    }

    if (this.sessions.length === 0) {
      this.createNewSession(false);
    } else {
      const lastSessionId = localStorage.getItem("aura_active_session") || this.sessions[0].id;
      const found = this.sessions.find(s => s.id === lastSessionId);
      this.selectSession(found ? found.id : this.sessions[0].id);
    }
  }

  saveSessions() {
    localStorage.setItem("aura_conversations", JSON.stringify(this.sessions));
    localStorage.setItem("aura_active_session", this.currentSessionId);
    this.renderSidebarHistory();
  }

  createNewSession(render = true) {
    const newId = "session_" + Date.now();
    const newSession = {
      id: newId,
      title: "Nueva Conversación",
      createdAt: new Date().toISOString(),
      messages: [
        {
          role: "bot",
          text: "¡Hola! Soy Aura, tu asistente e ingeniera de software. ¿En qué puedo colaborar o qué herramienta deseas configurar hoy?",
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]
    };

    this.sessions.unshift(newSession);
    this.currentSessionId = newId;
    this.saveSessions();

    if (render) {
      this.selectSession(newId);
    }
  }

  selectSession(sessionId) {
    const session = this.sessions.find(s => s.id === sessionId);
    if (!session) return;

    this.currentSessionId = sessionId;
    this.currentChatTitle.textContent = session.title;
    localStorage.setItem("aura_active_session", sessionId);

    // Renderizar mensajes de la sesión
    this.captionsStream.innerHTML = "";
    session.messages.forEach(m => {
      this.renderMessageBubble(m.role, m.text, m.time, false);
    });
    this.captionsStream.scrollTop = this.captionsStream.scrollHeight;

    this.renderSidebarHistory();
  }

  deleteSession(sessionId, event) {
    if (event) event.stopPropagation();
    this.sessions = this.sessions.filter(s => s.id !== sessionId);

    if (this.sessions.length === 0) {
      this.createNewSession();
    } else {
      if (this.currentSessionId === sessionId) {
        this.selectSession(this.sessions[0].id);
      } else {
        this.saveSessions();
      }
    }
  }

  renderSidebarHistory() {
    this.historyList.innerHTML = "";

    this.sessions.forEach(session => {
      const item = document.createElement("div");
      item.className = `history-item ${session.id === this.currentSessionId ? "active" : ""}`;
      item.onclick = () => this.selectSession(session.id);

      item.innerHTML = `
        <span class="history-title" title="${session.title}">${session.title}</span>
        <button class="history-delete-btn" title="Eliminar conversación" aria-label="Eliminar">🗑️</button>
      `;

      const delBtn = item.querySelector(".history-delete-btn");
      delBtn.onclick = (e) => this.deleteSession(session.id, e);

      this.historyList.appendChild(item);
    });
  }

  addMessageToCurrentSession(role, text) {
    const session = this.sessions.find(s => s.id === this.currentSessionId);
    if (!session) return;

    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    session.messages.push({ role, text, time });

    // Auto-generar título si es la primera pregunta del usuario
    if (role === "user" && (session.title === "Nueva Conversación" || session.title.startsWith("Conversación"))) {
      session.title = text.length > 28 ? text.substring(0, 28) + "..." : text;
      this.currentChatTitle.textContent = session.title;
    }

    this.saveSessions();
    this.renderMessageBubble(role, text, time, true);
  }

  /* ============================================================================
     3. RENDER MESSAGE BUBBLE WITH COPY BUTTON
     ============================================================================ */
  renderMessageBubble(role, text, time, autoScroll = true) {
    const bubble = document.createElement("div");
    bubble.className = `message-bubble ${role === "bot" ? "bot" : "user"}`;

    bubble.innerHTML = `
      <div class="bubble-header">
        <span class="bubble-name">${role === "bot" ? "🤖 Aura" : "👤 Tú"}</span>
        <div class="bubble-actions">
          <span class="bubble-time">${time || "Ahora"}</span>
          <button class="copy-msg-btn" title="Copiar mensaje">
            <span>📋</span> Copiar
          </button>
        </div>
      </div>
      <div class="bubble-text">${this.formatText(text)}</div>
    `;

    const copyBtn = bubble.querySelector(".copy-msg-btn");
    copyBtn.onclick = () => this.copyToClipboard(text, copyBtn);

    this.captionsStream.appendChild(bubble);
    if (autoScroll) {
      this.captionsStream.scrollTop = this.captionsStream.scrollHeight;
    }
  }

  formatText(text) {
    // Si contiene bloques de código o comandos
    return text.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
  }

  async copyToClipboard(text, btnElement) {
    try {
      await navigator.clipboard.writeText(text);
      btnElement.classList.add("copied");
      btnElement.innerHTML = "<span>✓</span> ¡Copiado!";
      setTimeout(() => {
        btnElement.classList.remove("copied");
        btnElement.innerHTML = "<span>📋</span> Copiar";
      }, 2000);
    } catch (e) {
      // Fallback
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);

      btnElement.classList.add("copied");
      btnElement.innerHTML = "<span>✓</span> ¡Copiado!";
      setTimeout(() => {
        btnElement.classList.remove("copied");
        btnElement.innerHTML = "<span>📋</span> Copiar";
      }, 2000);
    }
  }

  /* ============================================================================
     4. EVENT LISTENERS
     ============================================================================ */
  initEvents() {
    this.toggleSidebarBtn.addEventListener("click", () => {
      this.sidebar.classList.toggle("collapsed");
    });

    this.newChatBtn.addEventListener("click", () => {
      this.createNewSession();
    });

    this.toggleMicBtn.addEventListener("click", () => {
      if (!this.isConnected) {
        this.startSession();
      } else {
        this.stopSession();
      }
    });

    this.audioTestBtn.addEventListener("click", () => this.playAudioTest());
    
    this.clearCaptionsBtn.addEventListener("click", () => {
      const session = this.sessions.find(s => s.id === this.currentSessionId);
      if (session) {
        session.messages = [];
        this.saveSessions();
      }
      this.captionsStream.innerHTML = "";
    });

    window.addEventListener("resize", () => this.resizeCanvas());
  }

  resizeCanvas() {
    const rect = this.canvas.parentElement.getBoundingClientRect();
    this.canvas.width = rect.width;
    this.canvas.height = rect.height;
  }

  setStatus(state, label) {
    this.statusBadge.className = `status-badge ${state.toLowerCase()}`;
    this.statusText.textContent = label.toUpperCase();
  }

  /* ============================================================================
     5. SPEECH SYNTHESIS & RECOGNITION
     ============================================================================ */
  speakText(text) {
    if (!('speechSynthesis' in window)) return;
    
    window.speechSynthesis.cancel();

    // Limpiar posibles bloques de código de la locución hablada
    const cleanSpokenText = text.replace(/```[\s\S]*?```/g, ' Código adjunto en pantalla. ');

    const utterance = new SpeechSynthesisUtterance(cleanSpokenText);
    utterance.lang = "es-ES";
    utterance.rate = 1.05;
    utterance.pitch = 1.0;

    const voices = window.speechSynthesis.getVoices();
    const esVoice = voices.find(v => v.lang.startsWith("es") && (v.name.includes("Google") || v.name.includes("Natural") || v.name.includes("Paulina") || v.name.includes("Mónica") || v.name.includes("Jorge")));
    if (esVoice) {
      utterance.voice = esVoice;
    }

    utterance.onstart = () => {
      this.isSpeaking = true;
      this.setStatus("speaking", "Hablando");
    };

    utterance.onend = () => {
      this.isSpeaking = false;
      if (this.isConnected) {
        this.setStatus("connected", "Escuchando");
      }
    };

    utterance.onerror = () => {
      this.isSpeaking = false;
      if (this.isConnected) {
        this.setStatus("connected", "Escuchando");
      }
    };

    window.speechSynthesis.speak(utterance);
  }

  async startSession() {
    try {
      this.setStatus("listening", "Conectando...");
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
      if (this.audioContext.state === "suspended") {
        await this.audioContext.resume();
      }

      this.mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          sampleRate: 16000,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        }
      });

      this.audioInput = this.audioContext.createMediaStreamSource(this.mediaStream);
      this.analyser = this.audioContext.createAnalyser();
      this.analyser.fftSize = 256;
      this.dataArray = new Uint8Array(this.analyser.frequencyBinCount);

      this.audioInput.connect(this.analyser);

      this.processor = this.audioContext.createScriptProcessor(4096, 1, 1);
      this.processor.onaudioprocess = (e) => this.handleAudioInput(e);

      this.audioInput.connect(this.processor);
      this.processor.connect(this.audioContext.destination);

      this.initSpeechRecognition();
      this.connectWebSocket();

      this.isConnected = true;
      this.toggleMicBtn.className = "cta-button active";
      this.btnText.textContent = "DETENER CONVERSACIÓN";
      this.stageOverlay.classList.add("hidden");
      this.setStatus("connected", "En Línea");

      this.startActiveWaveform();
    } catch (err) {
      console.error("Error al acceder al micrófono:", err);
      this.setStatus("disconnected", "Error Micrófono");
      alert("Error al iniciar micrófono: " + err.message);
      this.stopSession();
    }
  }

  initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    this.recognition = new SpeechRecognition();
    this.recognition.lang = "es-ES";
    this.recognition.continuous = true;
    this.recognition.interimResults = false;
    this.recognition.maxAlternatives = 1;

    this.recognition.onresult = (event) => {
      const current = event.resultIndex;
      const transcript = event.results[current][0].transcript.trim();
      
      if (transcript.length > 0) {
        console.log("🗣️ Transcripción detectada:", transcript);
        this.addMessageToCurrentSession("user", transcript);

        // Enviar con contexto de sesión
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
          const session = this.sessions.find(s => s.id === this.currentSessionId);
          this.socket.send(JSON.stringify({
            type: "user_transcription",
            sessionId: this.currentSessionId,
            history: session ? session.messages.slice(-6) : [],
            text: transcript
          }));
        }
      }
    };

    this.recognition.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
    };

    this.recognition.onend = () => {
      if (this.isConnected && this.recognition) {
        try {
          this.recognition.start();
        } catch (e) {}
      }
    };

    try {
      this.recognition.start();
    } catch (e) {}
  }

  connectWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host = window.location.host || "localhost:8765";
    const wsUrl = `${protocol}//${host}/ws`;

    this.socket = new WebSocket(wsUrl);
    this.socket.binaryType = "arraybuffer";

    this.socket.onopen = () => {
      console.log("✅ WebSocket conectado.");
      this.setStatus("connected", "Escuchando");
    };

    this.socket.onmessage = (event) => {
      if (typeof event.data === "string") {
        try {
          const msg = JSON.parse(event.data);
          
          if (msg.type === "caption") {
            if (msg.text) {
              this.addMessageToCurrentSession(msg.role || "bot", msg.text);
              if (msg.speak) {
                this.speakText(msg.text);
              }
            }
          } else if (msg.type === "status") {
            if (msg.state === "thinking") {
              this.setStatus("listening", msg.label || "Pensando...");
            } else if (msg.state === "connected") {
              if (!this.isSpeaking) {
                this.setStatus("connected", msg.label || "Escuchando");
              }
            }
            this.updateProviders(msg);
          }
        } catch (e) {
          console.warn("Mensaje texto no JSON:", event.data);
        }
      } else if (event.data instanceof ArrayBuffer) {
        this.playAudioBuffer(event.data);
      }
    };

    this.socket.onclose = () => {
      if (this.isConnected) {
        this.setStatus("disconnected", "Desconectado");
      }
    };
  }

  updateProviders(msg) {
    if (msg.stt) document.getElementById("stt-val").textContent = msg.stt;
    if (msg.llm) document.getElementById("llm-val").textContent = msg.llm;
    if (msg.tts) document.getElementById("tts-val").textContent = msg.tts;
  }

  handleAudioInput(event) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;

    const inputData = event.inputBuffer.getChannelData(0);
    const pcm16 = new Int16Array(inputData.length);
    for (let i = 0; i < inputData.length; i++) {
      let s = Math.max(-1, Math.min(1, inputData[i]));
      pcm16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
    }
    this.socket.send(pcm16.buffer);
  }

  playAudioBuffer(arrayBuffer) {
    if (!this.audioContext) return;
    this.setStatus("speaking", "Hablando");
    this.isSpeaking = true;

    const pcm16 = new Int16Array(arrayBuffer);
    const audioBuffer = this.audioContext.createBuffer(1, pcm16.length, 16000);
    const channelData = audioBuffer.getChannelData(0);

    for (let i = 0; i < pcm16.length; i++) {
      channelData[i] = pcm16[i] / 32768.0;
    }

    const source = this.audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(this.audioContext.destination);
    source.onended = () => {
      this.isSpeaking = false;
      this.setStatus("connected", "Escuchando");
    };
    source.start();
  }

  playAudioTest() {
    const text = "¡Hola! La salida de audio de tus altavoces está funcionando perfectamente.";
    this.speakText(text);
    this.addMessageToCurrentSession("bot", "🔊 " + text);
  }

  stopSession() {
    this.isConnected = false;
    this.isSpeaking = false;

    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    if (this.recognition) {
      this.recognition.abort();
      this.recognition = null;
    }
    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach(t => t.stop());
    }
    if (this.audioContext) {
      this.audioContext.close();
    }
    if (this.socket) {
      this.socket.close();
    }
    cancelAnimationFrame(this.animationId);

    this.toggleMicBtn.className = "cta-button idle";
    this.btnText.textContent = "INICIAR CONVERSACIÓN";
    this.stageOverlay.classList.remove("hidden");
    this.setStatus("disconnected", "Desconectado");
    this.startIdleAnimation();
  }

  /* ============================================================================
     6. CANVAS WAVEFORM ANIMATION
     ============================================================================ */
  startActiveWaveform() {
    cancelAnimationFrame(this.animationId);

    const render = () => {
      this.animationId = requestAnimationFrame(render);
      if (!this.analyser) return;

      this.analyser.getByteFrequencyData(this.dataArray);
      const width = this.canvas.width;
      const height = this.canvas.height;
      this.canvasCtx.clearRect(0, 0, width, height);

      const style = getComputedStyle(document.documentElement);
      const colorStart = style.getPropertyValue("--waveform-gradient-start").trim() || "#6366f1";
      const colorMid = style.getPropertyValue("--waveform-gradient-mid").trim() || "#06b6d4";
      const colorEnd = style.getPropertyValue("--waveform-gradient-end").trim() || "#10b981";

      const gradient = this.canvasCtx.createLinearGradient(0, 0, width, 0);
      gradient.addColorStop(0, colorStart);
      gradient.addColorStop(0.5, colorMid);
      gradient.addColorStop(1, colorEnd);

      const barCount = 48;
      const barWidth = (width / barCount) * 0.7;
      const step = Math.floor(this.dataArray.length / barCount);

      for (let i = 0; i < barCount; i++) {
        const val = this.dataArray[i * step] || 0;
        const barHeight = Math.max(6, (val / 255) * (height * 0.75));
        const x = i * (width / barCount) + (width / barCount - barWidth) / 2;
        const y = height / 2 - barHeight / 2;

        this.canvasCtx.fillStyle = gradient;
        this.canvasCtx.shadowBlur = 12;
        this.canvasCtx.shadowColor = colorMid;
        this.canvasCtx.beginPath();
        this.canvasCtx.roundRect(x, y, barWidth, barHeight, 4);
        this.canvasCtx.fill();
      }

      this.phase += 0.05;
      this.canvasCtx.beginPath();
      this.canvasCtx.strokeStyle = colorStart;
      this.canvasCtx.lineWidth = 2;
      this.canvasCtx.shadowBlur = 8;
      this.canvasCtx.shadowColor = colorStart;

      for (let x = 0; x < width; x += 10) {
        const y = height / 2 + Math.sin(x * 0.02 + this.phase) * 12;
        if (x === 0) this.canvasCtx.moveTo(x, y);
        else this.canvasCtx.lineTo(x, y);
      }
      this.canvasCtx.stroke();
    };

    render();
  }

  startIdleAnimation() {
    cancelAnimationFrame(this.animationId);

    const render = () => {
      this.animationId = requestAnimationFrame(render);
      const width = this.canvas.width;
      const height = this.canvas.height;
      this.canvasCtx.clearRect(0, 0, width, height);

      this.phase += 0.02;
      this.canvasCtx.beginPath();
      this.canvasCtx.strokeStyle = "rgba(99, 102, 241, 0.25)";
      this.canvasCtx.lineWidth = 2;

      for (let x = 0; x < width; x += 10) {
        const y = height / 2 + Math.sin(x * 0.015 + this.phase) * 6;
        if (x === 0) this.canvasCtx.moveTo(x, y);
        else this.canvasCtx.lineTo(x, y);
      }
      this.canvasCtx.stroke();
    };

    render();
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.auraApp = new VoiceAgentApp();
});
