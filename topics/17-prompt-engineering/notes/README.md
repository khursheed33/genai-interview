# Prompt Engineering Notes

## Prompt structure
A robust prompt usually separates task, context, constraints, output format, and examples. Explicit acceptance criteria are more useful than vague instructions such as “be smart.”

## Few-shot and decomposition
Zero-shot gives instructions only. Few-shot adds examples that demonstrate the desired behavior. Decomposition breaks a complex task into smaller transformations. ReAct-style systems interleave reasoning/action steps, while modern implementations should expose only the required tool/action interface rather than relying on hidden reasoning text.

## Context engineering
Prompt quality includes what information is retrieved, ordered, summarized, filtered, and omitted. Long context should be curated, not simply stuffed into the window.

## Evaluation and versioning
Prompts are production artifacts. Version them, record model/settings, maintain regression datasets, compare variants, and monitor production behavior. DSPy and similar approaches treat prompting as an optimization/programming problem.

## Security
Treat external content as untrusted input. Prompt injection can attempt to override instructions or manipulate tool use. Use privilege separation, tool allowlists, validation, and output checks rather than assuming a prompt can provide a complete security boundary.

## Practice
Create zero/few-shot variants, build a structured extraction prompt, design a long-context summarization strategy, run an A/B prompt evaluation, and create an injection-resistant tool workflow.