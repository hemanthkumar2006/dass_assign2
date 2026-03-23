class RegistrationModule:
    def __init__(self):
        self.members = {}

    def register(self, name):
        if name in self.members:
            raise ValueError(f"{name} is already registered.")
        self.members[name] = {"role": None, "skill_level": 0}
        return f"Registered {name}."

