# Multimodal GenAI Notes

## Vision and documents
VLMs combine visual and language understanding. OCR extracts text but can lose layout; document AI often needs text, coordinates, tables, images, and page structure. Preserve provenance when converting documents into retrieval chunks.

## Speech
STT converts speech to text; TTS converts text to speech. Voice agents add turn detection, streaming, interruption/barge-in, tool calls, and latency constraints. A voice pipeline often has audio → STT → reasoning/tool layer → TTS.

## Image and video generation
Diffusion-based systems iteratively denoise representations toward an output conditioned by text or other inputs. Generation quality depends on model, conditioning, sampling, resolution, and safety controls. Video adds temporal consistency and substantially increases compute complexity.

## Specialized applications
Text-to-SQL translates natural language into database queries and therefore needs schema grounding, authorization, query validation, and limits. Code assistants need repository context, tool permissions, testing, and secret protection. Computer-use systems need strong action boundaries because UI actions can create side effects.

## Edge models
Small models trade capability for latency, privacy, cost, and offline operation. Quantization and distillation can make them practical on constrained hardware.

## Practice
Build a document extraction pipeline preserving layout, prototype a voice loop, test Text-to-SQL against a restricted schema, and design a safe computer-use action policy.