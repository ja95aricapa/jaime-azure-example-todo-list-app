import azure.functions as func
import json
from shared_code import db
from shared_code.utils import get_user_from_token


def main(req: func.HttpRequest) -> func.HttpResponse:
    user = get_user_from_token(req)
    if not user:
        return func.HttpResponse(json.dumps({"error": "Unauthorized"}), status_code=401)

    task_id = req.route_params.get("id")
    db.tasks.delete_item(item=task_id, partition_key=user["sub"])

    return func.HttpResponse(
        json.dumps({"message": "deleted"}), mimetype="application/json"
    )
