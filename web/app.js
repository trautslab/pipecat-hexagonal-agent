/**
 * Aura Voice AI - Web Client v1.1.0
 * Soporte para Persistencia en Servidor (Client-Agnostic Storage),
 * Consola Lateral Derecha en Tiempo Real, Numeración Correlativa por Turnos
 * y Sincronización Multi-Navegador / Multi-Dispositivo.
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
    this.activeTurnCounter = 0;

    // DOM Elements
    this.themeToggleBtn = document.getElementById("theme-toggle-btn");
    this.themeIcon = document.getElementById("theme-icon");
    this.toggleSidebarBtn = document.getElementById("toggle-sidebar-btn");
    this.sidebar = document.getElementById("sidebar");
    this.newChatBtn = document.getElementById("new-chat-btn");
    this.historyList = document.getElementById("history-list");
    this.currentChatTitle = document.getElementById("current-chat-title");

    // Right Console Sidebar DOM Elements
    this.toggleConsoleBtn = document.getElementById("toggle-console-btn");
    this.rightConsoleSidebar = document.getElementById("right-console-sidebar");
    this.closeConsoleBtn = document.getElementById("close-console-btn");
    this.copyConsoleBtn = document.getElementById("copy-console-btn");
    this.consoleEmptyState = document.getElementById("console-empty-state");
    this.consoleTurnsContainer = document.getElementById("console-turns-container");

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
     2. SESSIONS & PERSISTENCE (Backend Storage + Local Cache)
     ============================================================================ */
  async initSessions() {
    // 1. Cargar caché local inmediata
    const rawSessions = localStorage.getItem("aura_conversations");
    if (rawSessions) {
      try {
        this.sessions = JSON.parse(rawSessions);
      } catch (e) {
        this.sessions = [];
      }
    }

    // 2. Sincronizar con el Servidor Backend (/api/sessions)
    try {
      const res = await fetch("/api/sessions");
      if (res.ok) {
        const backendSessions = await res.json();
        if (Array.isArray(backendSessions) && backendSessions.length > 0) {
          this.sessions = backendSessions;
        }
      }
    } catch (err) {
      console.warn("No se pudo conectar con el endpoint de sesiones del backend:", err);
    }

    if (this.sessions.length === 0) {
      this.createNewSession(false);
    } else {
      const lastSessionId = localStorage.getItem("aura_active_session") || this.sessions[0].id;
      const found = this.sessions.find(s => s.id === lastSessionId);
      this.selectSession(found ? found.id : this.sessions[0].id);
    }
  }

  async saveSessions() {
    localStorage.setItem("aura_conversations", JSON.stringify(this.sessions));
    localStorage.setItem("aura_active_session", this.currentSessionId);
    this.renderSidebarHistory();

    // Sincronizar sesión activa en el servidor de forma asíncrona
    const currentSession = this.sessions.find(s => s.id === this.currentSessionId);
    if (currentSession) {
      try {
        await fetch("/api/sessions", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(currentSession)
        });
      } catch (e) {
        console.warn("Error guardando sesión en el servidor:", e);
      }
    }
  }

  createNewSession(render = true) {
    const newId = "session_" + Date.now();
    const newSession = {
      id: newId,
      title: "Nueva Conversación",
      createdAt: new Date().toISOString(),
      turnCounter: 1,
      messages: [
        {
          role: "bot",
          turnIndex: 1,
          text: "¡Hola! Soy Aura, tu asistente e ingeniera de software. Cuento con motor de razonamiento autónomo (ReAct), persistencia en servidor y consola de telemetría en vivo. ¿Qué deseas consultar o construir hoy?",
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          telemetry: null
        }
      ],
      consoleLogs: []
    };

    this.sessions.unshift(newSession);
    this.currentSessionId = newId;
    this.activeTurnCounter = 1;
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
    this.activeTurnCounter = session.turnCounter || session.messages.length;
    localStorage.setItem("aura_active_session", sessionId);

    // 1. Renderizar mensajes en el chat
    this.captionsStream.innerHTML = "";
    session.messages.forEach(m => {
      this.renderMessageBubble(m.role, m.text, m.time, false, m.turnIndex);
    });
    this.captionsStream.scrollTop = this.captionsStream.scrollHeight;

    // 2. Renderizar historial de consola derecha
    this.renderConsoleHistory(session);

    this.renderSidebarHistory();
  }

  async deleteSession(sessionId, event) {
    if (event) event.stopPropagation();
    this.sessions = this.sessions.filter(s => s.id !== sessionId);

    try {
      await fetch(`/api/sessions/${sessionId}`, { method: "DELETE" });
    } catch (e) {
      console.warn("Error eliminando sesión en el servidor:", e);
    }

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

  addMessageToCurrentSession(role, text, telemetry = null) {
    const session = this.sessions.find(s => s.id === this.currentSessionId);
    if (!session) return;

    if (!session.turnCounter) session.turnCounter = session.messages.length;
    session.turnCounter += 1;
    const turnIndex = session.turnCounter;

    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    session.messages.push({ role, text, time, turnIndex, telemetry });

    if (role === "user" && (session.title === "Nueva Conversación" || session.title.startsWith("Conversación"))) {
      session.title = text.length > 28 ? text.substring(0, 28) + "..." : text;
      this.currentChatTitle.textContent = session.title;
    }

    this.saveSessions();
    this.renderMessageBubble(role, text, time, true, turnIndex);
    return turnIndex;
  }

  /* ============================================================================
     3. RENDER MESSAGE BUBBLE IN CHAT
     ============================================================================ */
  renderMessageBubble(role, text, time, autoScroll = true, turnIndex = null) {
    const bubble = document.createElement("div");
    bubble.className = `message-bubble ${role === "bot" ? "bot" : "user"}`;

    const turnNum = turnIndex ? `#${turnIndex}` : "";

    bubble.innerHTML = `
      <div class="bubble-header">
        <div class="bubble-title-group">
          ${turnNum ? `<span class="turn-badge ${role}">${turnNum}</span>` : ""}
          <span class="bubble-name">${role === "bot" ? "🤖 Aura" : "👤 Tú"}</span>
        </div>
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
     4. RIGHT CONSOLE SIDEBAR
     ============================================================================ */
  renderConsoleHistory(session) {
    this.consoleTurnsContainer.innerHTML = "";
    const logs = session.consoleLogs || [];

    if (logs.length === 0) {
      this.consoleEmptyState.classList.remove("hidden");
      return;
    }

    this.consoleEmptyState.classList.add("hidden");
    logs.forEach(turnData => {
      this.renderTurnCardInConsole(turnData, false);
    });
    this.consoleTurnsContainer.scrollTop = this.consoleTurnsContainer.scrollHeight;
  }

  renderTurnCardInConsole(turnData, isOpen = true) {
    this.consoleEmptyState.classList.add("hidden");

    let card = document.getElementById(`turn-card-${turnData.turnIndex}`);
    if (!card) {
      card = document.createElement("details");
      card.id = `turn-card-${turnData.turnIndex}`;
      card.className = "console-turn-card active";
      if (isOpen) card.setAttribute("open", "");

      card.innerHTML = `
        <summary>
          <span>⚡ Turno #${turnData.turnIndex}</span>
          <span class="turn-tag-live" id="turn-tag-${turnData.turnIndex}">● Procesando en vivo...</span>
        </summary>
        <div class="console-turn-body" id="turn-body-${turnData.turnIndex}">
          <div class="console-turn-prompt">💬 <strong>Prompt:</strong> "${turnData.userPrompt || ''}"</div>
          <div class="console-steps-list" id="turn-steps-${turnData.turnIndex}"></div>
        </div>
      `;
      this.consoleTurnsContainer.appendChild(card);
    }

    const stepsList = card.querySelector(`#turn-steps-${turnData.turnIndex}`);
    if (stepsList && turnData.steps) {
      stepsList.innerHTML = "";
      turnData.steps.forEach(step => {
        let icon = "🧠";
        if (step.kind === "action") icon = "⚙️";
        if (step.kind === "observation") icon = "✅";

        const item = document.createElement("div");
        item.className = "console-step-item";
        item.innerHTML = `
          <span class="console-step-icon">${icon}</span>
          <div class="console-step-text">
            <strong>${step.title}:</strong> ${step.detail}
            ${step.timestamp ? `<div class="console-step-meta">[${step.timestamp}]</div>` : ''}
          </div>
        `;
        stepsList.appendChild(item);
      });
    }

    this.consoleTurnsContainer.scrollTop = this.consoleTurnsContainer.scrollHeight;
  }

  handleLiveTraceStep(turnIndex, step, timestamp, elapsedMs) {
    const session = this.sessions.find(s => s.id === this.currentSessionId);
    if (!session) return;

    if (!session.consoleLogs) session.consoleLogs = [];
    let turnEntry = session.consoleLogs.find(t => t.turnIndex === turnIndex);
    if (!turnEntry) {
      turnEntry = {
        turnIndex: turnIndex,
        timestamp: timestamp || new Date().toLocaleTimeString(),
        steps: [],
        status: "processing"
      };
      session.consoleLogs.push(turnEntry);
    }

    step.timestamp = timestamp;
    turnEntry.steps.push(step);
    this.saveSessions();

    this.renderTurnCardInConsole(turnEntry, true);
  }

  finalizeTurnInConsole(turnIndex, telemetry) {
    const session = this.sessions.find(s => s.id === this.currentSessionId);
    if (!session) return;

    if (!session.consoleLogs) session.consoleLogs = [];
    let turnEntry = session.consoleLogs.find(t => t.turnIndex === turnIndex);
    if (!turnEntry) {
      turnEntry = {
        turnIndex: turnIndex,
        timestamp: telemetry ? telemetry.timestamp : new Date().toLocaleTimeString(),
        steps: telemetry ? telemetry.steps : [],
        duration_ms: telemetry ? telemetry.duration_ms : 0
      };
      session.consoleLogs.push(turnEntry);
    } else if (telemetry) {
      turnEntry.duration_ms = telemetry.duration_ms;
      turnEntry.model = telemetry.model;
      turnEntry.files_affected = telemetry.files_affected;
    }

    turnEntry.status = "done";
    this.saveSessions();

    const tag = document.getElementById(`turn-tag-${turnIndex}`);
    if (tag) {
      tag.className = "turn-tag-live done";
      tag.textContent = `✓ Completado (${turnEntry.duration_ms || 0}ms)`;
    }

    const card = document.getElementById(`turn-card-${turnIndex}`);
    if (card) {
      card.classList.remove("active");
      const body = card.querySelector(".console-turn-body");
      if (body && !body.querySelector(".console-turn-meta-footer")) {
        const metaFooter = document.createElement("div");
        metaFooter.className = "console-turn-meta-footer";
        metaFooter.innerHTML = `
          <span>⏱️ Latencia: <strong>${turnEntry.duration_ms || 0}ms</strong></span>
          <span>🤖 Modelo: <strong>${turnEntry.model || "Llama 3.1 8B"}</strong></span>
        `;
        body.appendChild(metaFooter);
      }
    }
  }

  copyConsoleToClipboard() {
    const session = this.sessions.find(s => s.id === this.currentSessionId);
    if (!session || !session.consoleLogs || session.consoleLogs.length === 0) {
      alert("No hay registros de trazabilidad en la sesión activa.");
      return;
    }

    let md = `# ⚡ Consola de Trazabilidad Aura - Conversación: "${session.title}"\n`;
    md += `- **ID de Sesión:** \`${session.id}\`\n`;
    md += `- **Fecha:** ${session.createdAt}\n\n`;

    session.consoleLogs.forEach(turn => {
      md += `## 🔹 Turno #${turn.turnIndex} (${turn.timestamp})\n`;
      if (turn.userPrompt) md += `**Prompt Usuario:** "${turn.userPrompt}"\n\n`;
      md += `### 📋 Pasos ReAct Ejecutados:\n`;
      (turn.steps || []).forEach((s, idx) => {
        md += `${idx + 1}. **[${(s.kind || 'THOUGHT').toUpperCase()}] ${s.title}:** ${s.detail}\n`;
      });
      if (turn.duration_ms) md += `\n- **Latencia Total:** ${turn.duration_ms}ms\n`;
      if (turn.model) md += `- **Modelo:** ${turn.model}\n`;
      if (turn.files_affected && turn.files_affected.length > 0) {
        md += `- **Archivos Modificados:** ${turn.files_affected.join(", ")}\n`;
      }
      md += `\n---\n\n`;
    });

    this.copyToClipboard(md, this.copyConsoleBtn);
  }

  /* ============================================================================
     5. EVENT LISTENERS
     ============================================================================ */
  initEvents() {
    this.toggleSidebarBtn.addEventListener("click", () => {
      this.sidebar.classList.toggle("collapsed");
    });

    this.toggleConsoleBtn.addEventListener("click", () => {
      this.rightConsoleSidebar.classList.toggle("collapsed");
      this.toggleConsoleBtn.classList.toggle("active", !this.rightConsoleSidebar.classList.contains("collapsed"));
    });

    this.closeConsoleBtn.addEventListener("click", () => {
      this.rightConsoleSidebar.classList.add("collapsed");
      this.toggleConsoleBtn.classList.remove("active");
    });

    this.copyConsoleBtn.addEventListener("click", () => {
      this.copyConsoleToClipboard();
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
        session.consoleLogs = [];
        session.turnCounter = 0;
        this.saveSessions();
      }
      this.captionsStream.innerHTML = "";
      this.consoleTurnsContainer.innerHTML = "";
      this.consoleEmptyState.classList.remove("hidden");
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
     6. SPEECH SYNTHESIS & RECOGNITION
     ============================================================================ */
  speakText(text) {
    if (!('speechSynthesis' in window)) return;
    
    window.speechSynthesis.cancel();
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
        const userTurn = this.addMessageToCurrentSession("user", transcript);

        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
          const session = this.sessions.find(s => s.id === this.currentSessionId);
          this.socket.send(JSON.stringify({
            type: "user_transcription",
            sessionId: this.currentSessionId,
            turnIndex: userTurn,
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
      console.log("✅ WebSocket conectado con ReAct Live Streaming Console.");
      this.setStatus("connected", "Escuchando");
    };

    this.socket.onmessage = (event) => {
      if (typeof event.data === "string") {
        try {
          const msg = JSON.parse(event.data);
          
          if (msg.type === "turn_start") {
            const session = this.sessions.find(s => s.id === this.currentSessionId);
            if (session) {
              if (!session.consoleLogs) session.consoleLogs = [];
              const newTurn = {
                turnIndex: msg.turnIndex,
                timestamp: msg.timestamp,
                userPrompt: msg.userPrompt,
                steps: [],
                status: "processing"
              };
              session.consoleLogs.push(newTurn);
              this.saveSessions();
              this.renderTurnCardInConsole(newTurn, true);
            }
          } else if (msg.type === "live_trace_step") {
            this.handleLiveTraceStep(msg.turnIndex, msg.step, msg.timestamp, msg.elapsed_ms);
          } else if (msg.type === "caption") {
            if (msg.text) {
              const botTurn = this.addMessageToCurrentSession(msg.role || "bot", msg.text, msg.telemetry || null);
              this.finalizeTurnInConsole(msg.turnIndex, msg.telemetry);
              if (msg.speak) {
                this.speakText(msg.text);
              }
            }
          } else if (msg.type === "status") {
            if (msg.state === "thinking") {
              this.setStatus("listening", msg.label || "Razonando...");
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
     7. CANVAS WAVEFORM ANIMATION
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
