# login_api/error_handler/exceptions.py

class APIError(Exception):
    """Base API Error"""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv

# Domain-specific exceptions
class DatabaseError(APIError):
    """Database operation failed"""
    def __init__(self, message="Database error"):
        super().__init__(message, 500)