class CrewManagementModule:
    def __init__(self, registration_module):
        self.registration = registration_module
        self.valid_roles = ["driver", "mechanic", "strategist"]

    def assign_role(self, name, role, skill_level):
        if name not in self.registration.members:
            raise ValueError(f"{name} must be registered first.")
        if role not in self.valid_roles:
            raise ValueError(f"Invalid role: {role}")
        self.registration.members[name]["role"] = role
        self.registration.members[name]["skill_level"] = skill_level
        return f"Assigned {name} as {role}."

    def get_members_by_role(self, role):
        return [name for name, data in self.registration.members.items() if data["role"] == role]

