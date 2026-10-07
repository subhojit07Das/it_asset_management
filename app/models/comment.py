from datetime import datetime

class Comment:
    def __init__(self, text, author_name, author_role):
        self.text = text
        self.author_name = author_name
        self.author_role = author_role
        self.created_at = datetime.now()

    def __str__(self):
        time = self.created_at.strftime("%Y-%m-%d %H:%M")
        return f"[{time}] {self.author_name} ({self.author_role}): {self.text}"