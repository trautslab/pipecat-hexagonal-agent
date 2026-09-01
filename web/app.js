/**
 * Aura Voice AI - Web Client
 * Captura de micrófono con Web Audio API, visualizador de ondas en Canvas y streaming WebSocket.
 */

class VoiceAgentWebClient {
  constructor() {
    this.audioContext = null;
    this.mediaStream = null;
    this.audioInput = null;
    this.processor = null;
    this.analyser = null;
    this.socket = null;
    this.isPlaying = false;
    this.isConnected = false;

    // Elementos DOM
    this.toggleBtn = document.getElementById("toggle-mic-btn");
    this.btnText = document.getElementById("btn-text");
    this.statusBadge = document.getElementById("status-badge");
    this.statusText = document.getElementById("status-text");
    this.canvas = document.getElementById("waveform-canvas");
    this.canvasCtx = this.canvas.getContext("2d");
    this.overlay = document.getElementById("visualizer-overlay");
    this.captionsBox = document.getElementById("captions-box");

    this.animationId = null;
    this.dataArray = null;

    this.initEvents();
    this.drawIdleWaveform();
  }

  initEvents() {
    this.toggleBtn.addEventListener("click", () => {
      if (!this.isConnected) {
        this.startSession();
      } else {
        this.stopSession();
      }
    });

    window.addEventListener("resize", () => this.resizeCanvas());
    this.resizeCanvas();
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
    const item = document.createElement("div");
    item.className = `caption-item ${role === "bot" ? "bot-msg" : "user-msg"}`;
    
    const avatar = document.createElement("span");
    avatar.className = "avatar";
    avatar.textContent = role === "bot" ? "🤖 Aura:" : "👤 Tú:";

    const content = document.createElement("p");
    content.textContent = text;

    item.appendChild(avatar);
    item.appendChild(content);
    this.captionsBox.appendChild(item);
    this.captionsBox.scrollTop = this.captionsBox.scrollHeight;
  }

  async startSession() {
    try {
      this.setStatus("listening", "Conectando...");
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
      
      // Solicitar micrófono
      this.mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: 1,
          sampleRate: 16000,
          echoCancellation: true,
          noiseSuppression: true
        }
      });

      this.audioInput = this.audioContext.createMediaStreamSource(this.mediaStream);
      this.analyser = this.audioContext.createAnalyser();
      this.analyser.fftSize = 256;
      this.dataArray = new Uint8Array(this.analyser.frequencyBinCount);

      // Conexión de audio
      this.audioInput.connect(this.analyser);

      // Procesador de chunks de audio PCM
      this.processor = this.audioContext.createScriptProcessor(4096, 1, 1);
      this.processor.onaudioprocess = (e) => this.handleAudioProcess(e);
      
      this.audioInput.connect(this.processor);
      this.processor.connect(this.audioContext.destination);

      // Iniciar WebSocket
      this.connectWebSocket();

      // UI
      this.isConnected = true;
      this.toggleBtn.className = "mic-button active";
      this.btnText.textContent = "DETENER CONVERSACIÓN";
      this.overlay.classList.add("hidden");
      this.setStatus("connected", "Escuchando");

      this.startWaveformAnimation();
    } catch (err) {
      console.error("Error al iniciar sesión de audio:", err);
      this.setStatus("disconnected", "Error de micrófono");
      alert("No se pudo acceder al micrófono: " + err.message);
    }
  }

  connectWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host = window.location.host || "localhost:8765";
    const wsUrl = `${protocol}//${host}/ws`;

    this.socket = new WebSocket(wsUrl);
    this.socket.binaryType = "arraybuffer";

    this.socket.onopen = () => {
      console.log("WebSocket conectado con Aura Voice AI");
      this.setStatus("connected", "En Línea");
    };

    this.socket.onmessage = (event) => {
      if (typeof event.data === "string") {
        try {
          const msg = JSON.parse(event.data);
          if (msg.type === "caption") {
            this.addCaption("bot", msg.text);
          }
        } catch (e) {
          console.warn("Mensaje de texto no JSON:", event.data);
        }
      } else if (event.data instanceof ArrayBuffer) {
        this.playAudioBuffer(event.data);
      }
    };

    this.socket.onerror = (e) => {
      console.warn("WebSocket error:", e);
    };

    this.socket.onclose = () => {
      console.log("WebSocket cerrado.");
      if (this.isConnected) {
        this.setStatus("disconnected", "Desconectado");
      }
    };
  }

  handleAudioProcess(event) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) return;

    const inputData = event.inputBuffer.getChannelData(0);
    // Convertir Float32 a Int16 PCM binario
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
    
    // Interpretar PCM 16bit recibido y reproducir
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
      this.setStatus("connected", "Escuchando");
    };
    source.start();
  }

  stopSession() {
    this.isConnected = false;
    if (this.mediaStream) {
      this.mediaStream.getTracks().forEach(track => track.stop());
    }
    if (this.audioContext) {
      this.audioContext.close();
    }
    if (this.socket) {
      this.socket.close();
    }
    cancelAnimationFrame(this.animationId);

    this.toggleBtn.className = "mic-button idle";
    this.btnText.textContent = "INICIAR CONVERSACIÓN";
    this.overlay.classList.remove("hidden");
    this.setStatus("disconnected", "Desconectado");
    this.drawIdleWaveform();
  }

  startWaveformAnimation() {
    const draw = () => {
      this.animationId = requestAnimationFrame(draw);
      this.analyser.getByteFrequencyData(this.dataArray);

      const width = this.canvas.width;
      const height = this.canvas.height;
      this.canvasCtx.clearRect(0, 0, width, height);

      // Gradiente Neon
      const gradient = this.canvasCtx.createLinearGradient(0, 0, width, 0);
      gradient.addColorStop(0, "#6366f1");
      gradient.addColorStop(0.5, "#06b6d4");
      gradient.addColorStop(1, "#10b981");

      const barWidth = (width / this.dataArray.length) * 2.2;
      let x = 0;

      for (let i = 0; i < this.dataArray.length; i++) {
        const barHeight = (this.dataArray[i] / 255) * (height * 0.75);
        this.canvasCtx.fillStyle = gradient;
        this.canvasCtx.shadowBlur = 12;
        this.canvasCtx.shadowColor = "#06b6d4";
        this.canvasCtx.fillRect(x, height / 2 - barHeight / 2, barWidth - 2, barHeight);
        x += barWidth;
      }
    };
    draw();
  }

  drawIdleWaveform() {
    const width = this.canvas.width;
    const height = this.canvas.height;
    this.canvasCtx.clearRect(0, 0, width, height);
    
    this.canvasCtx.beginPath();
    this.canvasCtx.moveTo(0, height / 2);
    this.canvasCtx.lineTo(width, height / 2);
    this.canvasCtx.strokeStyle = "rgba(99, 102, 241, 0.25)";
    this.canvasCtx.lineWidth = 2;
    this.canvasCtx.stroke();
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.voiceClient = new VoiceAgentWebClient();
});
