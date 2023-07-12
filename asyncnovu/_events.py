import httpx
from asyncnovu._constants import Paths
from asyncnovu._utils import format
from asyncnovu.models import Trigger


# Trigger a notification workflow.
# [INFO] https://docs.novu.co/api/trigger-event/

async def trigger_event(self, trigger: Trigger):
    """
    Trigger a notification workflow.

            Parameters:
                    trigger (Trigger): Trigger request details to identify and configure the required Novu workflow.

            Returns:
                dict : The response from the server with acknowledgement if the request succeeded, error details if not.

            API Reference: https://docs.novu.co/api/trigger-event/

    """

    # Configuring request URL and payload data.
    url = self.api_url + Paths.TRIGGER_ENDPOINT
    json = {
        "name": trigger.id,
        "to": trigger.subscribers,
        "payload": trigger.payload,
        "overrides": trigger.overrides,
    }

    # Post the request to Novu server.
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=json, headers=self.headers)
        return format(response.status_code, response.json())


# Broadcast a notification to all existing subscribers.
# [INFO] https://docs.novu.co/api/broadcast-event-to-all/

async def broadcast_event(self, trigger: Trigger):
    """
    Broadcast a notification to all existing subscribers.

            Parameters:
                    trigger (Trigger): Trigger request details to identify and configure the required Novu workflow.

                    NOTE: Omit the 'subscribers' field from the Trigger object as it will not be used.

            Returns:
                dict : The response from the server with acknowledgement if the request succeeded, error details if not.

            API Reference: https://docs.novu.co/api/broadcast-event-to-all/

    """

    # Configuring request URL and payload data.
    url = self.api_url + Paths.TRIGGER_ENDPOINT + Paths.BROADCAST_SUFFIX
    json = {
        "name": trigger.id,
        "payload": trigger.payload,
        "overrides": trigger.overrides,
    }

    # Post the request to Novu server.
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=json, headers=self.headers)
        return format(response.status_code, response.json())


# Cancel any active or pending notification workflow using a previously generated transaction ID.
# [INFO] https://docs.novu.co/api/cancel-triggered-event/

async def cancel_event(self, transaction_id):
    """
    Cancel any active or pending notification workflow using a previously generated transaction ID.

            Parameters:
                    transaction_id (str): Unique trnasaction ID of the workflow to be cancelled.

            Returns:
                dict : The response from the server with acknowledgement if the request succeeded, error details if not.

            API Reference: https://docs.novu.co/api/cancel-triggered-event/

    """

    # Configuring request URL and payload data.
    url = self.api_url + Paths.TRIGGER_ENDPOINT + f"/{transaction_id}"

    # Post the request to Novu server.
    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=self.headers)
        return format(response.status_code, response.json())
