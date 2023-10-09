from dataclasses import dataclass


@dataclass
class MailEmitter:
    display_name: str
    email: str

    def pretty_display(self):
        return f"{self.display_name} <{self.email}>"


david_emitter = MailEmitter("David de Puzzle Cook", "david@puzzlecook.com")
contact_emitter = MailEmitter("Puzzle Cook", "contact@puzzlecook.com")
