from src.database import Database
from src.utils import generate_uuid, hash_new_password, is_correct_password
def ResponseWrapper(payload):
    return {
        "data": payload
    }

class logic:
    def user_login(payload):
        # required
        # {
        #     "username": "",
        #     "password": "",
        # }

        # validation

        d = Database("user")
        user = d.get_single_data_by_username(payload["username"])
        if not user:
            return {"error": "user not exist"}

        if not is_correct_password(salt=user["salt"], password=payload["password"], pw_from_db=user["password"]):
            return {"error": "user pw incorrect"}


        return ResponseWrapper(user)
        
    def user_create(payload):
        # required
        # {
        #     "username": "",
        #     "password": "",
        #     "name": "",
        #     "appointment": ""
        # }

        # validation



        # 

        payload["id"] = generate_uuid()
        salt, pw_hash = hash_new_password(payload["password"])
        payload["password"] = str(pw_hash)
        payload["salt"] = str(salt)

        # database insert
        d = Database("user")
        d.insert_data(payload)
        return ResponseWrapper(payload)