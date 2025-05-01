class Admin:
    def __init__(self, admin_user_id, admin_name=None):
        self.admin_user_id = admin_user_id
        self.admin_name = admin_name

    def to_dict(self):
        return {
            "admin_user_id" : self.admin_user_id,
            "admin_name" : self.admin_name,
        }

