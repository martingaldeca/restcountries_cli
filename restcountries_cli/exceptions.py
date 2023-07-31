class NotValidEndpoint(Exception):
    """
    Exception that will be raised if the endpoint used in the api is not valid
    """


class APIException(Exception):
    """
    Exception that will be raised if API experienced an internal error
    """
