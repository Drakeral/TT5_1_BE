from src.database import Database
from src.utils import generate_uuid, hash_new_password, is_correct_password, validate_requre_field
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