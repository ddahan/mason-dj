from dataclasses import dataclass


@dataclass
class MailEmitter:
    display_name: str
    email: str

    def pretty_display(self):
        return f"{self.display_name} <{self.email}>"


david_emitter = MailEmitter("David de Mason", "david@mason.io")
contact_emitter = MailEmitter("Mason Team", "contact@mason.io")
