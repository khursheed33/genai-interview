# GenAI Evaluation Notes

## Evaluation layers
Evaluate individual components and the whole system. Offline evaluation uses fixed datasets before release; online evaluation observes real traffic with suitable privacy controls.

## Metrics
For retrieval, use Recall@k, MRR, and NDCG. For text overlap, BLEU/ROUGE can be useful but are limited for semantic quality. BERTScore compares semantic representations. For RAG, separately measure retrieval relevance, context quality, faithfulness/grounding, and answer relevance.

## LLM judges
LLM-as-judge can scale qualitative assessment but is itself a model with bias, calibration, and consistency concerns. Use clear rubrics, blinded comparisons where practical, multiple examples, and periodic human review.

## Agent evaluation
Measure task success, tool correctness, unnecessary calls, latency, cost, failure recovery, and safety violations. A successful final answer can still hide a dangerous or expensive trajectory.

## Regression system
Maintain a versioned golden dataset. Record model, prompt, retrieval configuration, tools, and evaluator versions. Set thresholds and investigate regressions rather than relying on one aggregate score.

## Practice
Create 30–50 representative cases, score retrieval and generation separately, compare two prompt versions, calibrate an LLM judge against human labels, and add safety cases.