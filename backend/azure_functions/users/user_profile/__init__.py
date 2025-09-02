import azure.functions as func
import json
from shared_code import db
from shared_code.utils import get_user_from_token


def main(req: func.HttpRequest) -> func.HttpResponse:
    user = get_user_from_token(req)
    if not user:
        return func.HttpResponse(json.dumps({"error": "Unauthorized"}), status_code=401)

    body = req.get_json()
    user_id = user["sub"]

    # Como la partición es /email, usamos el email del token
    existing = db.users.read_item(item=user_id, partition_key=user["email"])

    if "name" in body:
        existing["name"] = body["name"]
    if "email" in body:
        existing["email"] = body[
            "email"
        ]  # ⚠️ cambiar email implica cambiar partition key en un diseño real

    db.users.upsert_item(existing)

    return func.HttpResponse(
        json.dumps({"message": "Perfil actualizado", "user": existing}),
        mimetype="application/json",
    )
