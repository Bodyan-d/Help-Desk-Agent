
from google.genai import types

TOOL_DECLARATIONS = [
    types.FunctionDeclaration(
        name="get_booking",
        description="Get booking details by booking ID.",
        parameters_json_schema={
            "type": "object",
            "properties": {
                "booking_id": {
                    "type": "string",
                    "description": "Booking ID, e.g. CW-1001"
                }
            },
            "required": ["booking_id"]
        }
    ),

    types.FunctionDeclaration(
        name="calculate_refund",
        description=(
            "Calculate the cancellation refund for a booking. "
            "Use this tool for refund amounts."
        ),
        parameters_json_schema={
            "type": "object",
            "properties": {
                "booking_id": {
                    "type": "string"
                }
            },
            "required": ["booking_id"]
        }
    ),

    types.FunctionDeclaration(
        name="search_policies",
        description=(
            "Search CityWheels policies for prices, "
            "opening hours, cancellation rules and FAQs."
        ),
        parameters_json_schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Customer question to search for"
                }
            },
            "required": ["query"]
        }
    )
]

GEMINI_TOOLS = [
    types.Tool(function_declarations=TOOL_DECLARATIONS)
]
