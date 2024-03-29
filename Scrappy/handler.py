import json
import traceback
from platforms.clubv1.tee_times import handle as handle_clubv1


def handle(event, context):
    """
    {
        "platform": "clubv1",
        "url": "https://www.example.com/lkjlkj",
        "date": "2021-12-25"
    }
    """
    try:
        print(event)
        body = json.loads(event.get("body"))
        print(body)
        platform = body.get("platform")
        if platform == "clubv1":
            print(*"Handling clubv1 platform")
            return handle_clubv1(body)
        else:
            print("Unsupported platform")
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Unsupported platform"}),
            }
    except Exception as e:
        error_message = "An error occurred while processing the request."
        print(error_message)
        print(traceback.format_exc())
        return {"statusCode": 500, "body": json.dumps({"message": error_message})}
