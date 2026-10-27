
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from .tools import get_booking, calculate_refund, search_policies
from .tool_definitions import GEMINI_TOOLS

load_dotenv()

TOOLS = {
    "get_booking": get_booking,
    "calculate_refund": calculate_refund,
    "search_policies": search_policies,
}

SYSTEM_PROMPT = """
You are a helpful customer support agent for CityWheels.

Rules:
- Answer only questions about CityWheels.
- Use tools to retrieve policies and booking information.
- Never invent facts, prices or booking details.
- Always use calculate_refund for refund amounts.
- Never calculate refunds yourself.
- If information is missing, tell the customer to contact
  help@citywheels.example.
- Do not claim that a booking has been cancelled.
- Refund calculations use the fixed date from the assignment.
"""


def run_agent(question: str, client=None, max_steps: int = 5) -> str:
    if client is None:
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

    history = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=question)]
        )
    ]

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=GEMINI_TOOLS,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
        thinking_config=types.ThinkingConfig(
            thinking_level=types.ThinkingLevel.LOW
        )
    )

    for _ in range(max_steps):
        response = client.models.generate_content(
            model=model,
            contents=history,
            config=config
        )

        if not response.candidates or not response.candidates[0].content:
            return "Sorry, I could not generate an answer."

        model_content = response.candidates[0].content
        history.append(model_content)

        function_calls = response.function_calls or []
        print(function_calls)
        if not function_calls:
            return response.text or "Sorry, no answer was generated."

        tool_responses = [_handle_tool_call(call) for call in function_calls]
        
        print("tool_responses:", tool_responses)

        history.append(
            types.Content(
                role="user",
                parts=tool_responses
            )
        )

    return "Sorry, I could not complete the request."


def _handle_tool_call(call):
    name = call.name if isinstance(call.name, str) else "unknown"
    arguments = dict(call.args or {})

    print(f"[TOOL CALL] {name}: {arguments}")

    if name not in TOOLS:
        result = {"error": "Unknown tool"}
    else:
        result = _invoke_tool(name, arguments)

    return types.Part.from_function_response(
        name=name,
        response={"result": result}
    )


def _invoke_tool(name, arguments):
    try:
        if name in {"calculate_refund", "get_booking"}:
            arguments = {"booking_id": arguments["booking_id"]}
        elif name == "search_policies":
            arguments = {"query": arguments["query"]}

        return TOOLS[name](**arguments)
    except (KeyError, TypeError, ValueError) as error:
        return {"error": f"Invalid tool arguments: {error}"}


if __name__ == "__main__":
    print("CityWheels Help Desk Agent")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        try:
            answer = run_agent(question)
            print(f"\nAgent: {answer}")

        except Exception as error:
            print(f"\nAPI error: {error}")
