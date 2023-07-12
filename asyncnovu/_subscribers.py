import httpx
from asyncnovu._constants import Paths
from asyncnovu._utils import format


# Update an existing subscriber profile. If the subscriber foes not exist, a new one will be created.
# [INFO] https://docs.novu.co/api/update-subscriber/

async def upsert_subscriber(
    self,
    subscriber_id: str,
    email: str = None,
    first_name: str = None,
    last_name: str = None,
    phone: str = None,
    avatar: str = None,
):
    """
    Update an existing subscriber profile. If the subscriber does not exist, a new one will be created.

            Parameters:
                    subscriber_id (str): Unique ID of the subscriber.
                    email (str): Optional email address for the subscriber.
                    first_name (str): Optional first name of the subscriber.
                    last_name (str): Optional last name of the subscriber.
                    phone (str): Optional phone number of the subscriber.
                    avatar (str): Optional URL pointing to a profile picture.

            Returns:
                dict : The response from the server with the full profile dataset if the request succeeded, error details if not.

            API Reference:
                https://docs.novu.co/api/update-subscriber/

    """

    # Configuring request URL and payload data.
    url = self.api_url + Paths.SUBSCRIPTION_ENDPOINT
    json = {
        "subscriberId": subscriber_id,
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "phone": phone,
        "avatar": avatar,
    }

    # Post the request to Novu server.
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=json, headers=self.headers)
        return format(response.status_code, response.json())


# Delete an existing subscriber profile.
# [INFO] https://docs.novu.co/api/delete-subscriber/

async def delete_subscriber(
    self,
    subscriber_id: str,
):
    """
    Delete an existing subscriber profile.

            Parameters:
                    subscriber_id (str): Unique ID of the subscriber.

            Returns:
                dict : The response from the server with acknowledgement if the request succeeded, error details if not.

            API Reference:
                https://docs.novu.co/api/delete-subscriber/

    """

    # Configuring request URL and payload data.
    url = self.api_url + Paths.SUBSCRIPTION_ENDPOINT + f"/{subscriber_id}"

    # Post the request to Novu server.
    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=self.headers)
        return format(response.status_code, response.json())
