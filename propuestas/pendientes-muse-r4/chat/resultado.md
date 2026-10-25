# Resultado final de la evaluacion real del chat (ronda 4)

Modelo configurado final: gemma-4-31b-it (preferencia explicita del usuario; SOLO ese) | Triples: 284810 intactos

## Preferencia final

- Gemma 4 31B queda como unico valor de `ONTO_LLM_MODEL` en `.env`
  (gemini-3.1-flash-lite -> gemma-4-31b-it, solo esa linea).
- Respaldo original `.env.antes-r4-chat` (gemini-3.5-flash) NO sobrescrito.
- Sin mas llamadas en esta fase: ni contexto gigante ni sondas a Gemma.
  El integrador ampliara el parche de recuperacion-f2 (contexto acotado) y hara
  pruebas espaciadas conforme TPM; cuando haya parche acotado probado sin modelo,
  la raiz encargara un ensayo real espaciado.
- No volver a Gemini 3.1 ni proponer otro modelo.

## Corridas archivadas (todas conservadas)

- `antes-cambio-modelo/`: gemini-3.5-flash (C2 falla-oraculo honesta, C3 probado; 1x503, 3x429 diaria).
- `ensayo-gemma4/`: gemma-4-31b-it (sonda 200; C1 503, C2 429 TPM 16000/min, resto pendiente_cuota).
- `ensayo-gemini31/`: gemini-3.1-flash-lite (3 probado, 2 falla_oraculo, C6 429 TPM).
- Manejo de contexto demostrado en corridas 3.5 y 3.1 (citas de conteos, F2, diccionario).

## Configuracion activa y capas

- El sidecar fija el modelo al arrancar; el chat real toma Gemma4 tras reinicio de
  Studio (8137, integrador). NO reiniciado; ver `reinicio-requerido.json`. Sin UI desde OpenCode.
- Harness = modulos retrieval + model-client reutilizados (no E2E, no binario, no UI).
  studio-ui: leida por integrador, no enviada.

## Aclaracion de interrupcion UI

El usuario aclara que NUNCA presiono Escape; el aviso de la herramienta UI fue
interrupcion tecnica, no cancelacion humana. No se atribuye pausa al usuario.
