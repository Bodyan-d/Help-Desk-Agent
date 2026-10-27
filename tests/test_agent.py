
from types import SimpleNamespace
from google.genai import types

from src.agent import run_agent


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
