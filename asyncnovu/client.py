from asyncnovu._constants import Paths


# Python client for connecting and making requests to a Novu server.
class NovuClient:
    """
    A class to interface with Novu APIs and execute different operations.

    Parameters:

    api_key (str): Unique Novu API key to authorize requests to the Novu server.
    api_url (str): Novu Server URL for sending requests. If not provided, default value would be https://api.novu.co/v1

    """

    def __init__(self, api_key: str, api_url: str = Paths.API_URL):
        self.api_url = api_url
        self.headers = {
            "Authorization": f"ApiKey {api_key}",
            "Content-Type": "application/json",
        }
    
    from asyncnovu._events import trigger_event, bulk_trigger, broadcast_event, cancel_event
    from asyncnovu._subscribers import upsert_subscriber, delete_subscriber
