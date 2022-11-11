class APIError(Exception):
    """All custom API Exceptions"""
    pass


class APINotFoundError(APIError):
    """Custom Not Found Error Class."""
    code = 404
    description = "Not found"


class APIInvalidError(APIError):
    """Custom Invalid Error Class."""
    code = 400
    description = "Invalid"
