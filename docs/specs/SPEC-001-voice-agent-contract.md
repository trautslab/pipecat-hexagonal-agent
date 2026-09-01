# 📝 Especificación Técnica: SPEC-001 - Contrato de Puertos, Pipeline y Sesión Conversacional

- **ID:** `SPEC-001`
- **Estado:** `APPROVED`
- **Fecha:** 2026-09-01
- **Autor:** Ingeniero de Software Principal

---

## 1. Resumen
Esta especificación define los contratos formales para el agente de voz con Pipecat bajo arquitectura hexagonal.

---

## 2. Requerimientos Funcionales y Criterios BDD

```gherkin
Feature: Pipeline Conversacional Desacoplado con Pipecat

  Scenario: Inyección de Puertos y Construcción del Pipeline
    Given que se instancian los adaptadores de STTPort, LLMPort, TTSPort y TransportPort
    When el orquestador VoiceAgentPipelineBuilder inicializa el pipeline
    Then el pipeline contiene 7 elementos encadenados (Input -> STT -> UserAggregator -> LLM -> TTS -> Output -> AssistantAggregator)
    And no existen dependencias cruzadas entre el Core y los Adaptadores
```

---

## 3. Interfaces de Dominio

### Contrato STTPort
```python
class STTPort(ABC):
    @abstractmethod
    def get_service(self) -> Any: ...
    @property
    @abstractmethod
    def provider_name(self) -> str: ...
```

### Contrato LLMPort
```python
class LLMPort(ABC):
    @abstractmethod
    def get_service(self) -> Any: ...
    @abstractmethod
    def get_system_prompt(self) -> str: ...
    @property
    @abstractmethod
    def provider_name(self) -> str: ...
```

### Contrato TTSPort
```python
class TTSPort(ABC):
    @abstractmethod
    def get_service(self) -> Any: ...
    @property
    @abstractmethod
    def provider_name(self) -> str: ...
```

### Contrato TransportPort
```python
class TransportPort(ABC):
    @abstractmethod
    def get_input(self) -> Any: ...
    @abstractmethod
    def get_output(self) -> Any: ...
    @abstractmethod
    def get_transport(self) -> Any: ...
    @property
    @abstractmethod
    def provider_name(self) -> str: ...
```
