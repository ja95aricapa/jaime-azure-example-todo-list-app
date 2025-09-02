import azure.functions as func
import json, uuid
from shared_code import db


def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    email = body.get("email")
    password = body.get("password")
    name = body.get("name")

    if not email or not password:
        return func.HttpResponse(
            json.dumps({"error": "email y password requeridos"}),
            status_code=400,
            mimetype="application/json",
        )

    user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "password": password,  # ⚠️ usa bcrypt en prod
        "name": name,
    }

    db.users.create_item(user)
    return func.HttpResponse(
        json.dumps({"message": "usuario creado", "id": user["id"]}),
        mimetype="application/json",
    )
