from app.models import model


def get_datum(users):
    if users is None:
        return

    results = []
    for user in users:
        datum = {
            "id": str(user["id"]),
            "email": user["email"],
            "project_id": user["project_id"],
            "created_at": str(user["created_at"]),
        }
        results.append(datum)
    return results


def user_id_by_project(project_id):
    try:
        user = model.get_by_condition(
            table="user", field="project_id", value=f"{project_id}"
        )
        user_id = user[0]["id"]
        return user_id
    except IndexError:
        raise ValueError(f"User Not Found")
