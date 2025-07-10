class NotFoundError(Exception):
    """Raised when a resource is not found"""
    pass

class ValidationError(Exception):
    """Raised when input validation fails"""
    pass
