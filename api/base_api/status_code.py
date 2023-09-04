class StatusCode:
    """
    Коды http status code
    """
    SUCCESS = 200
    ADDED = 201
    ACCEPTED = 202
    NO_CONTENT = 204

    INCORRECT_HEADER = 400
    BAD_CREDENTIALS = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405

    INTERNAL_SERVER_ERROR = 500


status_code = StatusCode
