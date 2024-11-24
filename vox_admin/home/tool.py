class Tool:
    def __init__(self, name, status="stopped"):
        self.name = name
        self.status = status

    def to_dict(self):
        return {
            "name": self.name,
            "status": self.status,
        }

    def update_status(self, new_status):
        if new_status in ["running", "stopped"]:
            self.status = new_status
            return True
        return False
