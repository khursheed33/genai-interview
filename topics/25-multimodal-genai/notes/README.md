# Multimodal GenAI Notes

## Vision and documents
VLMs combine visual and language understanding. OCR extracts text but can lose layout; document AI may need text, coordinates, tables, images, and page structure. Preserve provenance when converting documents into retrieval chunks.

## Speech
STT converts speech to text; TTS converts text to speech. Voice agents add turn detection, streaming, interruption, tool calls, and strict latency requirements.

## Image and video
Diffusion systems iteratively denoise toward an output conditioned by text or other inputs. Video adds temporal consistency and much greater compute complexity.

## Specialized systems
Text-to-SQL needs schema grounding, authorization, query validation, and limits. Code assistants need repository context, tool permissions, tests, and secret protection. Computer-use systems require strong action boundaries because UI actions can create side effects.

## Edge models
Small models trade capability for latency, privacy, cost, and offline operation. Quantization and distillation can reduce resource requirements.

## Practice
Build document extraction preserving layout, prototype a voice loop, test Text-to-SQL against a restricted schema, and design a safe computer-use policy.