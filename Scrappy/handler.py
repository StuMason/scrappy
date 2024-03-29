import json
import traceback
from platforms.clubv1.tee_times import handle as handle_clubv1


def handle(event, context):
    try:
        """
        {
            "platform": "clubv1",
            "url": "https://www.example.com/lkjlkj",
            "date": "2021-12-25"
        }
        """
        platform = event.get("platform")
        if platform == "clubv1":
            return handle_clubv1(event)
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Unsupported platform"}),
            }
    except Exception as e:
        error_message = "An error occurred while processing the request."
        print(error_message)
        print(traceback.format_exc())
        return {"statusCode": 500, "body": json.dumps({"message": error_message})}
