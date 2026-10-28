import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from src.agent import run_agent

FOLDER = Path(__file__).resolve().parent


def contains_phrase(answer, phrase):
    
    pattern = rf"(?<!\w){re.escape(phrase)}(?!\w)"
    return re.search(pattern, answer, re.IGNORECASE) is not None


def check_answer(case, answer, calls):
    errors = []
    names = [call["name"] for call in calls]

    for tool in case["tools"]:
        if tool not in names:
            errors.append(f"Missing tool: {tool}")

    if "booking_id" in case:
        if not any(call["args"].get("booking_id") == case["booking_id"] for call in calls):
            errors.append(f"Wrong booking ID: expected {case['booking_id']}")

    for alternatives in case["contains"]:
        if not any(contains_phrase(answer, text) for text in alternatives):
            errors.append(f"Missing one of: {alternatives}")

    return errors


def save_results(results, model):
    passed = sum(not errors for _, _, _, errors in results)
    lines = [
        "# CityWheels evaluation",
        "",
        f"Date: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "Business-rule clock: 2026-06-10 09:00 +02:00",
        f"Model: {model}",
        f"Passed: {passed}/{len(results)}",
        "",
    ]
    for case, answer, calls, errors in results:
        lines += [
            f"## {'PASS' if not errors else 'FAIL'} — {case['id']}",
            f"Question: {case['question']}",
            f"Tools: {', '.join(call['name'] for call in calls) or '(none)'}",
            f"Problems: {'; '.join(errors) or '(none)'}",
            "Answer:",
            *(f"> {line}" for line in (answer or '(empty)').splitlines()),
            "",
        ]
    (FOLDER / "results.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", help="ID of one test case")
    args = parser.parse_args()

    cases = json.loads((FOLDER / "cases.json").read_text(encoding="utf-8"))
    if args.case:
        cases = [case for case in cases if case["id"] == args.case]
        if not cases:
            parser.error("Unknown case ID")

    load_dotenv()
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    results = []
    try:
        for case in cases:
            calls = []
            try:
                answer = run_agent(case["question"], client=client, tool_calls=calls)
                errors = check_answer(case, answer, calls)
            except Exception as exc:
                answer = ""
                errors = [f"Agent error: {type(exc).__name__}: {exc}"]

            results.append((case, answer, calls, errors))
            save_results(results, model)
            print(f"{'PASS' if not errors else 'FAIL'} — {case['id']}")
            for error in errors:
                print(f"  {error}")
    finally:
        client.close()

    passed = sum(not errors for _, _, _, errors in results)
    print(f"\nPassed: {passed}/{len(results)}. See eval/results.md")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
