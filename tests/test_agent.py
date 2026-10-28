
from types import SimpleNamespace
from google.genai import types

from src.agent import run_agent, _handle_tool_call, _invoke_tool


class FakeModels:
    def __init__(self):
        self.calls = 0

    def generate_content(self, *, model, contents, config):
        self.calls += 1

        if self.calls == 1:
            tool_call = types.FunctionCall(
                name="calculate_refund",
                args={"booking_id": "CW-1002"}
            )

            return SimpleNamespace(
                candidates=[
                    SimpleNamespace(
                        content=types.Content(
                            role="model",
                            parts=[
                                types.Part(function_call=tool_call)
                            ]
                        )
                    )
                ],
                function_calls=[tool_call],
                text=None
            )

        tool_result = (
            contents[-1]
            .parts[0]
            .function_response
            .response["result"]
        )

        assert tool_result["total_refund_eur"] == 340.0

        return SimpleNamespace(
            candidates=[
                SimpleNamespace(
                    content=types.Content(
                        role="model",
                        parts=[
                            types.Part.from_text(
                                text="Your refund is 340 EUR."
                            )
                        ]
                    )
                )
            ],
            function_calls=[],
            text="Your refund is 340 EUR."
        )


class FakeClient:
    def __init__(self):
        self.models = FakeModels()


def test_agent_calls_refund_tool():
    client = FakeClient()

    result = run_agent(
        "How much will I get back for CW-1002?",
        client=client
    )

    assert result == "Your refund is 340 EUR."
    assert client.models.calls == 2



def test_unknown_tool():
    fake_call = types.FunctionCall(
        name="delete_all_bookings",
        args={}
    )

    response = _handle_tool_call(fake_call)

    function_response = response.function_response

    assert function_response is not None
    assert function_response.response is not None

    result = function_response.response["result"]

    assert result["error"] == "Unknown tool"


def test_missing_tool_arguments():
    result = _invoke_tool(
        "calculate_refund",
        {}
    )

    assert "error" in result
    assert "Invalid tool arguments" in result["error"]


def test_unknown_booking_through_tool():
    result = _invoke_tool(
        "get_booking",
        {"booking_id": "CW-9999"}
    )

    assert result["error"] == "Booking not found"
    assert result["booking_id"] == "CW-9999"
    
class FakeInfiniteModels:
    def __init__(self):
        self.calls = 0

    def generate_content(self, *, model, contents, config):
        self.calls += 1

        tool_call = types.FunctionCall(
            name="get_booking",
            args={"booking_id": "CW-1001"}
        )

        return SimpleNamespace(
            candidates=[
                SimpleNamespace(
                    content=types.Content(
                        role="model",
                        parts=[
                            types.Part(function_call=tool_call)
                        ]
                    )
                )
            ],
            function_calls=[tool_call],
            text=None
        )
        

def test_agent_max_steps():
    client = SimpleNamespace(
        models=FakeInfiniteModels()
    )

    result = run_agent(
        "Find booking CW-1001",
        client=client,
        max_steps=3
    )

    assert client.models.calls == 3
    assert result == "Sorry, I could not complete the request."
