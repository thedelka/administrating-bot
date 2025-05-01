class Dialogue:

    current_num = 1

    def __init__(self, dialogue_messages_history : list, dialogue_status = "OPEN"):
        self.dialogue_id = Dialogue.current_num
        self.dialogue_messages_history = dialogue_messages_history
        self.dialogue_status = dialogue_status

        Dialogue.current_num += 1
