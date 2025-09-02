import azure.functions as func
import json, jwt, datetime, os
from shared_code import db

SECRET = os.getenv("JWT_SECRET", "supersecret")


def main(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_json()
    email = body.get("email")
    password = body.get("password")

    query = "SELECT * FROM c WHERE c.email=@e"
    params = [{"name": "@e", "value": email}]
    items = list(
        db.users.query_items(
            query=query, parameters=params, enable_cross_partition_query=True
        )
    )

    if not items or items[0]["password"] != password:
        return func.HttpResponse(
            json.dumps({"error": "Credenciales inválidas"}),
            status_code=401,
            mimetype="application/json",
        )

    payload = {
        "sub": items[0]["id"],
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, SECRET, algorithm="HS256")

    return func.HttpResponse(json.dumps({"token": token}), mimetype="application/json")
