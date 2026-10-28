# CityWheels Help Desk Agent — Solution

## Overview

This is a command-line customer support agent written in Python. It answers questions using CityWheels policy documents and booking data, rather than relying on the language model's general knowledge. It uses Google Gemini with function calling.

## Setup

Recommended: Python 3.11+ (developed and tested on Python 3.14.2).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create `.env` from `.env.example` and set your own API key:

```dotenv
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

Run the agent:

```powershell
python -m src.agent
```

Run tests and evaluation:

```powershell
python -m pytest -v
python -m eval.run_eval
python -m eval.run_eval --case refund_half
```

Evaluation results are saved in `eval/results.md`. The evaluation calls the real Gemini API; unit tests and FakeClient tests do not.

## Architecture

- `src/agent.py` — sends user questions to Gemini, handles requested function calls, and returns final answers.
- `src/tool_definitions.py` — declares tools and their input schemas for Gemini.
- `src/tools.py` — implements the Python tools.
- `src/helpers.py`, `src/base_words.py` — tokenize policy text and normalize selected words.
- `data/policies/*.md`, `data/bookings.json` — CityWheels sources.
- `tests/` — Python and agent-loop tests.
- `eval/` — real-model evaluation cases, runner and saved results.

### Agent loop

1. `run_agent(question)` sends the user's question, system instructions and tool declarations to Gemini.
2. Gemini either returns a final answer or requests one or more tools.
3. Python validates the requested tool name and allowed arguments, then executes the real function.
4. The function result is appended to the conversation history and sent back to Gemini.
5. The loop continues until there is a final answer or `max_steps` is reached.

Automatic SDK function execution is disabled so the application controls tool execution. For tests, a fake client can be injected into `run_agent()` without an API key or network calls.

### Tools

| Tool | Purpose |
| --- | --- |
| `search_policies(query)` | Search sections of the Markdown policies using token overlap and weighted headings. |
| `get_booking(booking_id)` | Read a booking from JSON or return `Booking not found`. |
| `calculate_refund(booking_id)` | Compute refunds in Python using a fixed clock and the cancellation rules. |

Refund calculations use the assignment's **fixed date: 2026-06-10 09:00 +02:00**, not the computer's real clock. Only confirmed bookings are eligible for cancellation. Rental refunds are 100% at least 48 hours before the start, 50% from 24 to less than 48 hours, and 0% below 24 hours. For eligible cancellation, the deposit is fully refunded; the booking fee is not. Non-confirmed bookings cannot be cancelled again and receive no cancellation refund.

The tool calculates a hypothetical refund; **it does not cancel a booking**.

## Model and design choices

I chose **Google Gemini 3.5 Flash-Lite** because it supports function calling and performed quickly in my local tests. An earlier Gemini model produced high-demand `503` errors and slow responses. The provider/model can be changed through configuration, though SDK-specific changes may be needed for other providers.

I used the direct Google SDK instead of LangChain or LangGraph. With only three tools and a simple loop, the SDK is easier to follow, debug and test. A local model (e.g. Ollama) would be possible, but would require additional setup and model-quality testing.

The system prompt limits answers to CityWheels, prohibits invented facts and instructs the agent to refer unknown questions to staff. These instructions reduce risk but do not guarantee perfect answers.

## Testing

Run all tests with `python -m pytest -v`.

- Tool tests cover booking lookup, refund amounts and boundaries (including exactly 24 and 48 hours), text normalization and policy retrieval.
- Agent tests inject `FakeClient` instead of calling Gemini. They check a complete tool-call cycle, unknown tools, missing arguments, unknown booking IDs and `max_steps`.

A fake model checks that Python correctly handles tool requests; it does **not** demonstrate that the real LLM chooses the correct tool. That is why I also run real-model evaluation.

## Evaluation

`eval/cases.json` contains **18 scenarios** (policies, bookings, refunds and refusals). `eval/run_eval.py` sends each question to the real agent, checks expected tools/booking IDs and selected answer phrases, and writes `eval/results.md`.

**Final run:** Passed: 17/18 
**That one failed:** 
```
FAIL — refuse_offtopic
Question: What is the capital of Australia?
Tools: (none)
Problems: Missing one of: ['contact', 'help@citywheels.example']
Answer:
> I can only help you with questions about CityWheels, our bike rentals, policies, and your bookings. For questions about general knowledge like the capital of Australia, I'm unable to assist!.
```

Earlier evaluation: **15/17 automated checks passed**. One correct answer about a missing booking was marked wrong because the evaluator did not recognize the phrase “unable to find”; I expanded the accepted phrases. Another scenario failed due to a Windows network connection error, rather than an incorrect answer. Manual review also spotted an unnecessary age-related recommendation that had passed keyword checks, so I adjusted the prompt to discourage unrequested alternatives.

The checks are heuristic: they can reject a correct paraphrase or accept an answer containing the expected keyword alongside an incorrect claim. Results still require manual review. The latest committed `eval/results.md` is the source of truth for the final run.

## How I used AI coding assistants

I used ChatGPT mainly for brainstorming the initial project structure, discussing implementation approaches, and getting explanations of unfamiliar concepts related to AI agents.

Initially, ChatGPT suggested a very simple structure with most of the logic in a single Python file. I decided to separate the agent loop, tool definitions, business logic, and helper functions into different modules to make the code easier to understand, test, and maintain.

Another challenge was choosing the LLM. ChatGPT initially suggested older Gemini models that were no longer available through my API access, followed by newer, more powerful models that experienced high demand, slow responses, and occasional 503 UNAVAILABLE errors.

From my practical experience at GlobalLogic, I understood that smaller, less complex tasks with a simple processing pipeline do not always require powerful models. Since the agent only needs to understand customer questions, select tools, and formulate answers, while Python handles the calculations, I chose Gemini 3.5 Flash-Lite. It provided much faster responses and was sufficient for this project's requirements.

## Limitations and next steps

- Policy retrieval is simple keyword-based ranking, so unfamiliar paraphrases may retrieve irrelevant sections.
- The LLM can still produce incorrect extra statements; system instructions are not formal guarantees.
- Evaluation primarily checks tool names and text fragments, not full semantic correctness.
- The CLI handles each question separately; follow-up conversation memory is not implemented.
- API connectivity, rate limits and provider availability affect end-to-end runs.
- Booking data is static JSON; the agent only reads it and does not create, modify or cancel bookings.

With more time, I would add better retrieval tests, structured output validation, more evaluation cases and conversation memory. A GitHub Actions workflow could run the offline tests on every push.
