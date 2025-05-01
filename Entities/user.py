from typing import Optional
class User:

    def __init__(self, user_id, user_name, message_history : Optional[list] = None):
        if message_history is None:
            message_history = []

        self.user_id = user_id
        self.user_name = user_name
        self.user_message_history = message_history