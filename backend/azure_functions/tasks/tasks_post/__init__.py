import azure.functions as func
import json, uuid
from shared_code import db
from shared_code.utils import get_user_from_token


def main(req: func.HttpRequest) -> func.HttpResponse:
    user = get_user_from_token(req)
    if not user:
        return func.HttpResponse(json.dumps({"error": "Unauthorized"}), status_code=401)

    body = req.get_json()
    task = {
        "id": str(uuid.uuid4()),
        "title": body.get("title"),
        "status": body.get("status", "pending"),
        "userId": user["sub"],
    }
    db.tasks.create_item(task)
    return func.HttpResponse(json.dumps(task), mimetype="application/json")
