def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]) if "_id" in user else None,  # Verifica si _id está en el diccionario
        "username": user["username"],
        "email": user["email"],
    }
