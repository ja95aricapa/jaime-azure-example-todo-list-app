import azure.functions as func
import json
from shared_code import db
from shared_code.utils import get_user_from_token


def main(req: func.HttpRequest) -> func.HttpResponse:
    user = get_user_from_token(req)
    if not user:
        return func.HttpResponse(json.dumps({"error": "Unauthorized"}), status_code=401)

    query = "SELECT * FROM c WHERE c.userId=@uid"
    params = [{"name": "@uid", "value": user["sub"]}]
    items = list(
        db.tasks.query_items(
            query=query, parameters=params, enable_cross_partition_query=True
        )
    )

    return func.HttpResponse(json.dumps(items), mimetype="application/json")
