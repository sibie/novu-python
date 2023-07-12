class Paths:
    """Collection of Novu API strings for making requests to the server."""

    API_URL = "https://api.novu.co/v1"

    # Base Endpoints
    TRIGGER_ENDPOINT = "/events/trigger"
    SUBSCRIBERS_ENDPOINT = "/subscribers"

    # Events
    BULK_SUFFIX = "/bulk"
    BROADCAST_SUFFIX = "/broadcast"

    # Subscribers
    CREDENTIALS_SUFFIX = "/credentials"
