class APIResponse:
    def __init__(self,data,message,status_code,success):
        self.data = data
        self.message = message
        self.status_code = status_code
        self.success = success

    def to_dict(self):
        return {"data": self.data, "message": self.message, "status_code": self.status_code, "success": self.success}