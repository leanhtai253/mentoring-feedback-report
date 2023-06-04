class successResponse:
    def __init__(self, code, message=None):
        self.code = code
        self.message = message

class errorResponse:
    def __init__(self, code, message=None):
        self.code = code
        self.message = message