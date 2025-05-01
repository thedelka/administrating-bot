from typing import Optional
from Entities.dialogue import Dialogue
class User:

    def __init__(self, user_id, user_name, dialogues : Optional[list[Dialogue]] = None):
        self.user_id = user_id
        self.user_name = user_name
        self.user_dialogues = dialogues