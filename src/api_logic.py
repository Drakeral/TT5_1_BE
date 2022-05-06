from src.database import Database
from src.utils import generate_uuid, hash_new_password, is_correct_password, validate_requre_field, get_datetime
def ResponseWrapper(payload):
    return {
        "data": payload
    }

class logic:
    def user_login(payload):

        # validation
        required = ["username", "password"]
        if not validate_requre_field(payload, required):
            return {"error": "missing field required"}

        d = Database("user")
        user = d.get_single_data_by_username(payload["username"])
        if not user:
            return {"error": "user does not exist"}

        if not is_correct_password(salt=user["salt"], password=payload["password"], pw_from_db=user["password"]):
            return {"error": "user pw incorrect"}


        return ResponseWrapper(user)
        
    def user_create(payload):

        # validation
        required = ["username", "password", "name", "appointment"]
        if not validate_requre_field(payload, required):
            return {"error": "missing field required"}

        payload["id"] = generate_uuid()
        salt, pw_hash = hash_new_password(payload["password"])
        payload["password"] = str(pw_hash)
        payload["salt"] = str(salt)

        # database insert
        d = Database("user")
        d.insert_data(payload)
        return ResponseWrapper(payload)








    def project_list():
        d = Database("project")
        return ResponseWrapper(d.get_multiple_data())

    def project_get(id):
        d = Database("project")
        return ResponseWrapper(d.get_single_data(id))
    
    def project_create(payload):
        # change according depend on frontend payload
        # payload = payload["formData"]

        # validation
        required = ["name", "description", "budget"]
        if not validate_requre_field(payload, required):
            return {"error": "missing field required"}

        payload["id"] = generate_uuid()

        d = Database("project")
        d.insert_data(payload)
        return {"func":"project_create", "payload": payload}

    def project_update(id, payload):
        
        d = Database("project")
        d.update_or_create(id, payload)
        return {"func":"project_update", "payload": payload}

    def project_delete(id):
        d = Database("project")
        d.remove_data(id)
        return {"func":"project_delete", "payload": id}








    def category_list():
        d = Database("category")
        return ResponseWrapper(d.get_multiple_data())

    def category_get(id):
        d = Database("category")
        return ResponseWrapper(d.get_single_data(id))
    
    def category_create(payload):
        # change according depend on frontend payload
        # payload = payload["formData"]

        # validation
        required = ["name"]
        if not validate_requre_field(payload, required):
            return {"error": "missing field required"}

        payload["id"] = generate_uuid()

        d = Database("category")
        d.insert_data(payload)
        return {"func":"category_create", "payload": payload}

    def category_update(id, payload):
        
        d = Database("category")
        d.update_or_create(id, payload)
        return {"func":"category_update", "payload": payload}

    def category_delete(id):
        d = Database("category")
        d.remove_data(id)
        return {"func":"category_delete", "payload": id}








    def expense_list():
        d = Database("expense")
        return ResponseWrapper(d.get_multiple_data())

    def expense_get(id):
        d = Database("expense")
        return ResponseWrapper(d.get_single_data(id))
    
    def expense_create(payload):
        # change according depend on frontend payload
        # payload = payload["formData"]

        # validation
        required = ["name", "description", "amount", "project_id", "category_id", "user_id"]
        if not validate_requre_field(payload, required):
            return {"error": "missing field required"}
        
        current_datetime = get_datetime()
        user_id = payload["user_id"]
        u_db = Database("user")
        user = u_db.get_single_data(user_id)
        if not user:
            return {"error": "user_id not exist"}
        current_user = user["name"]
        payload["id"] = generate_uuid()
        payload["created_at"] = current_datetime
        payload["created_by"] = current_user
        payload["updated_at"] = current_datetime
        payload["updated_by"] = current_user
        

        d = Database("expense")
        d.insert_data(payload)
        return {"func":"expense_create", "payload": payload}

    def expense_update(id, payload):
        
        # validation
        required = ["name", "description", "amount", "project_id", "category_id", "user_id"]
        if not validate_requre_field(payload, required):
            return {"error": "missing field required"}

        user_id = payload["user_id"]
        u_db = Database("user")
        user = u_db.get_single_data(user_id)
        if not user:
            return {"error": "user_id not exist"}
        current_user = user["name"]

        payload["updated_at"] = get_datetime()
        payload["updated_by"] = current_user
        d = Database("expense")
        expense_db = d.get_single_data(id)

        payload["created_at"] = expense_db["created_at"]
        payload["created_by"] = expense_db["created_by"]

        d.update_or_create(id, payload)
        return {"func":"expense_update", "payload": payload}

    def expense_delete(id):
        d = Database("expense")
        d.remove_data(id)
        return {"func":"expense_delete", "payload": id}