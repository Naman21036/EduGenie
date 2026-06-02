import json

def parse_json_response(content):

    try:

        content = content.strip()

        if content.startswith("```json"):

            content = content.replace(
                "```json",
                ""
            )

            content = content.replace(
                "```",
                ""
            ).strip()

        return json.loads(content)

    except Exception as e:

        return {
            "error": str(e),
            "raw_response": content
        }