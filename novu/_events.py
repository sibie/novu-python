import httpx
from novu._constants import Paths
from novu._utils import format


# Trigger a notification workflow.
# [INFO] https://docs.novu.co/api/trigger-event/

async def trigger_event(
    self,
    trigger_id: str,
    subscribers: list[str],
    payload: dict = None,
    overrides: dict = None,
):
    """
    Trigger a notification workflow.

            Parameters:
                    trigger_id (str): Unique ID of the Novu template.
                    subscribers (list[str]): List of subscriber IDs for users requiring notifications.
                    payload (dict): Optional dictionary with custom attributes needed by the template.
                    overrides (dict): Additional attributes needed for template integrations.

            Returns:
                dict : The response from the server with acknowledgement if the request succeeded, error details if not.

            API Reference: https://docs.novu.co/api/trigger-event/

    """

    # Configuring request URL and payload data.
    url = self.api_url + Paths.TRIGGER_ENDPOINT
    json = {
        "name": trigger_id,
        "to": subscribers,
        "payload": payload,
        "overrides": overrides,
    }

    # Post the request to Novu server.
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=json, headers=self.headers)
        return format(response.status_code, response.json())


# Broadcast a notification to all existing subscribers.
# [INFO] https://docs.novu.co/api/broadcast-event-to-all/

async def broadcast_event(
    self,
    trigger_id: str,
    payload: dict = None,
    overrides: dict = None,
):
    """
    Broadcast a notification to all existing subscribers.

            Parameters:
                    trigger_id (str): Unique ID of the Novu template.
                    payload (dict): Optional dictionary with custom attributes needed by the template.
                    overrides (dict): Additional attributes needed for template integrations.

            Returns:
                dict : The response from the server with acknowledgement if the request succeeded, error details if not.

            API Reference: https://docs.novu.co/api/broadcast-event-to-all/

    """

    # Configuring request URL and payload data.
    url = self.api_url + Paths.BROADCAST_ENDPOINT
    json = {
        "name": trigger_id,
        "payload": payload,
        "overrides": overrides,
    }

    # Post the request to Novu server.
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=json, headers=self.headers)
        return format(response.status_code, response.json())


# Cancel any active or pending notification workflow using a previously generated transaction ID.
# [INFO] https://docs.novu.co/api/cancel-triggered-event/

async def cancel_event(
    self,
    transaction_id,
):
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
