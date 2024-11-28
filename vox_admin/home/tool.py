from datetime import datetime, timedelta

class Tool:
    def __init__(self, id, name, status="stopped"):
        self.id = id
        self.name = name
        self.status = status
        if status == "running":
            self.exec_time = datetime.now()
        else:
            self.exec_time = None

    def to_dict(self):
        runtime = None
        if self.status == "running" and self.exec_time:
            total_seconds = int((datetime.now() - self.exec_time).total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            runtime = f"{minutes}:{seconds:02d}"

        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "runtime": runtime,
        }

    def turn_on(self):
        if self.status == "stopped":
            self.status = "running"
            self.exec_time = datetime.now()

    def turn_off(self):
        if self.status == "running":
            self.status = "stopped"
            self.exec_time = None

    def __str__(self):
        return f"{self.id}, {self.name}, {self.status}"
