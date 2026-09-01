/**
 * Aura Voice AI - Web Client v0.3.0
 * Soporte para Light/Dark Mode, visualizador de ondas reactivo en Canvas y streaming WebSocket.
 */

class VoiceAgentApp {
  constructor() {
    this.audioContext = null;
    this.mediaStream = null;
    this.audioInput = null;
    this.processor = null;
    this.analyser = null;
    this.socket = null;
    this.isConnected = false;
    this.isSpeaking = false;

    // DOM Elements
    this.themeToggleBtn = document.getElementById("theme-toggle-btn");
    this.themeIcon = document.getElementById("theme-icon");
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
     2. EVENT LISTENERS & RESIZE
     ============================================================================ */
  initEvents() {
    this.toggleMicBtn.addEventListener("click", () => {
      if (!this.isConnected) {
        this.startSession();
      } else {
        this.stopSession();
      }
    });

    this.audioTestBtn.addEventListener("click", () => this.playAudioTest());
    
    this.clearCaptionsBtn.addEventListener("click", () => {
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

  addCaption(role, text) {
    const bubble = document.createElement("div");
    bubble.className = `message-bubble ${role === "bot" ? "bot" : "user"}`;

    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    bubble.innerHTML = `
      <div class="bubble-header">
        <span class="bubble-name">${role === "bot" ? "🤖 Aura" : "👤 Tú"}</span>
        <span class="bubble-time">${now}</span>
      </div>
      <p class="bubble-text">${text}</p>
    `;

    this.captionsStream.appendChild(bubble);
    this.captionsStream.scrollTop = this.captionsStream.scrollHeight;
  }

  /* ============================================================================
     3. AUDIO SESSION & WEBSOCKET
     ============================================================================ */
  async startSession() {
    try {
      this.setStatus("listening", "Conectando...");
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
      if (this.audioContext.state === "suspended") {
        await this.audioContext.resume();
      }

      // 1. Obtener micrófono
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

      // 2. Procesador PCM de audio
      this.processor = this.audioContext.createScriptProcessor(4096, 1, 1);
      this.processor.onaudioprocess = (e) => this.handleAudioInput(e);

      this.audioInput.connect(this.processor);
      this.processor.connect(this.audioContext.destination);

      // 3. Conectar WebSocket
      this.connectWebSocket();

      // UI
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

  connectWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host = window.location.host || "localhost:8765";
    const wsUrl = `${protocol}//${host}/ws`;

    this.socket = new WebSocket(wsUrl);
    this.socket.binaryType = "arraybuffer";

    this.socket.onopen = () => {
      console.log("✅ WebSocket conectado a Aura Voice Agent.");
      this.setStatus("connected", "Escuchando");
    };

    this.socket.onmessage = (event) => {
      if (typeof event.data === "string") {
        try {
          const msg = JSON.parse(event.data);
          if (msg.type === "caption") {
            this.addCaption(msg.role || "bot", msg.text);
          } else if (msg.type === "status") {
            this.updateProviders(msg);
          }
        } catch (e) {
          console.warn("Mensaje texto no JSON:", event.data);
        }
      } else if (event.data instanceof ArrayBuffer) {
        this.playAudioBuffer(event.data);
      }
    };

    this.socket.onerror = (err) => {
      console.warn("WebSocket error:", err);
    };

    this.socket.onclose = () => {
      console.log("WebSocket cerrado.");
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
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = "sine";
      osc.frequency.setValueAtTime(440, ctx.currentTime); // Nota La 440Hz
      osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.3);

      gain.gain.setValueAtTime(0.2, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start();
      osc.stop(ctx.currentTime + 0.5);

      this.addCaption("bot", "🔊 Prueba de audio de altavoces ejecutada correctamente.");
    } catch (e) {
      alert("Error en prueba de audio: " + e.message);
    }
  }

  stopSession() {
    this.isConnected = false;
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
     4. WAVEFORM VISUALIZER RENDERING (Canvas)
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

      // Calcular gradiente según tema
      const style = getComputedStyle(document.documentElement);
      const colorStart = style.getPropertyValue("--waveform-gradient-start").trim() || "#6366f1";
      const colorMid = style.getPropertyValue("--waveform-gradient-mid").trim() || "#06b6d4";
      const colorEnd = style.getPropertyValue("--waveform-gradient-end").trim() || "#10b981";

      const gradient = this.canvasCtx.createLinearGradient(0, 0, width, 0);
      gradient.addColorStop(0, colorStart);
      gradient.addColorStop(0.5, colorMid);
      gradient.addColorStop(1, colorEnd);

      // 1. Barras de Frecuencia
      const barCount = 48;
      const barWidth = (width / barCount) * 0.7;
      const step = Math.floor(this.dataArray.length / barCount);

      for (let i = 0; i < barCount; i++) {
        const val = this.dataArray[i * step] || 0;
        const barHeight = Math.max(4, (val / 255) * (height * 0.75));
        const x = i * (width / barCount) + (width / barCount - barWidth) / 2;
        const y = height / 2 - barHeight / 2;

        this.canvasCtx.fillStyle = gradient;
        this.canvasCtx.shadowBlur = 10;
        this.canvasCtx.shadowColor = colorMid;
        this.canvasCtx.beginPath();
        this.canvasCtx.roundRect(x, y, barWidth, barHeight, 4);
        this.canvasCtx.fill();
      }

      // 2. Onda Suave Continua (Sine Wave Overlay)
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
