# CityWheels Help Desk Agent

A command-line AI support assistant for **CityWheels**, a fictional bike rental company. The agent uses **Google Gemini function calling** to answer questions using the company's policy documents and booking records. Refund amounts are calculated in Python, not by the language model.

## Features

- Answers questions about rental prices, opening hours, age restrictions, deposits and cancellation policies.
- Retrieves booking details by booking ID.
- Calculates cancellation refunds using deterministic Python rules.
- Handles unknown bookings and questions outside the available CityWheels information.
- Includes offline tests and a real-model evaluation suite.

## Project structure

```text
.
├── data/
│   ├── bookings.json
│   └── policies/
│       ├── cancellations.md
│       ├── faq.md
│       └── prices.md
├── src/
│   ├── agent.py              # CLI and manual tool-calling loop
│   ├── tool_definitions.py   # Function schemas sent to Gemini
│   ├── tools.py              # Booking lookup, policy search, refund logic
│   ├── helpers.py            # Text processing
│   └── base_words.py         # Synonyms and stop words
├── tests/
│   ├── test_agent.py         # Fake-LLM agent tests
│   └── test_tools.py         # Unit tests
├── eval/
│   ├── cases.json            # Real-model evaluation questions
│   ├── run_eval.py           # Evaluation runner
│   └── results.md            # Saved evaluation results
├── .env.example
├── requirements.txt
└── SOLUTION.md               # Design decisions, findings and limitations
```

## Requirements

- Python 3.11 or newer (developed on Python 3.14)
- A [Google Gemini API key](https://aistudio.google.com/apikey) for the CLI and real-model evaluation

## Installation

Clone the repository and open its directory. Then create a virtual environment and install dependencies.

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and provide your own key:

```dotenv
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

**Do not commit `.env` or any real API keys.**

## Run the agent

```bash
python -m src.agent
```

Example question:

```text
You: How much would I get back if I cancel CW-1002?
```

The agent uses the refund tool to compute **340 EUR** for this sample booking (40 EUR rental refund + 300 EUR deposit; the booking fee is not refunded). Type `exit` to quit.

**Important:** All refund calculations use the dataset's fixed date and time, **2026-06-10 09:00 Europe/Warsaw (UTC+02:00)**, rather than the current system time. The agent estimates refunds but **does not cancel bookings**.

## Tests

Run all offline tests with command:

```bash
python -m pytest -v
```

`tests/test_tools.py` checks policy search, booking lookup and refund rules. `tests/test_agent.py` uses a fake Gemini client to test the agent's tool-calling loop, invalid tool requests and step limits. **These tests do not require an API key or network access.**

## Evaluation

Run the real Gemini evaluation:

```bash
python -m eval.run_eval
```

Or run one case:

```bash
python -m eval.run_eval --case refund_half
```

Test cases are defined in `eval/cases.json`; results are written to `eval/results.md`. This evaluation **requires an API key and internet access**. Automatic text checks are heuristic, so review questionable answers manually.

## CI (GitHub Actions)

The workflow in `.github/workflows/tests.yml` runs **offline pytest tests** on each push and pull request. It deliberately does **not** run real Gemini evaluation or require an API key.

## More information

See [SOLUTION.md](SOLUTION.md) for architecture, model selection, testing methodology, evaluation findings, AI assistant usage and known limitations.
