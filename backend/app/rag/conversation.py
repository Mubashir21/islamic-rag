MAX_MESSAGES = 6


class Conversation:
    def __init__(self):
        self.messages: list[dict] = []
        self.last_chunks: list[dict] = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > MAX_MESSAGES:
            self.messages = self.messages[-MAX_MESSAGES:]

    def update_chunks(self, chunks: list[dict]):
        self.last_chunks = chunks

    def get_history(self) -> list[dict]:
        return self.messages

    def is_empty(self) -> bool:
        return len(self.messages) == 0
