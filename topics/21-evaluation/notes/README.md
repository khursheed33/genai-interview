# GenAI Evaluation Notes

## Layers
Evaluate components and the whole system. Offline evaluation uses fixed datasets before release; online evaluation observes production behavior with suitable privacy controls.

## Metrics
For retrieval use Recall@k, MRR, and NDCG. BLEU/ROUGE measure lexical overlap; BERTScore measures semantic similarity. For RAG, separately measure retrieval relevance, context quality, faithfulness/grounding, and answer relevance.

## LLM judges
LLM-as-judge scales qualitative assessment but has bias and consistency limits. Use clear rubrics, calibration against human labels, and periodic human review.

## Agent evaluation
Measure task success, tool correctness, unnecessary calls, latency, cost, and safety violations. A successful final answer can still hide an unsafe or wasteful trajectory.

## Regression
Maintain a versioned golden dataset and record model, prompt, retrieval, tool, and evaluator versions. Set thresholds and investigate regressions rather than relying on one aggregate score.

## Practice
Create representative cases, score retrieval and generation separately, compare prompt versions, calibrate a judge, and add safety cases.