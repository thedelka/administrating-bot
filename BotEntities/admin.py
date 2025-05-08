class Admin:
    def __init__(self, admin_user_id, admin_name=None, texting_user_id : list[int] = None):
        if texting_user_id is None:
            texting_user_id = []

        self.admin_user_id = admin_user_id
        self.admin_name = admin_name
        self.texting_user_id = texting_user_id
        self.admin_queries_count = len(self.texting_user_id)
        self.is_ready_for_work = False
