class Trigger:
    """
    Class representing a single trigger request to activate a Novu workflow from an existing template.

    Attributes:

    id (str): Unique ID of the Novu template.
    subscribers (list[str]): List of subscriber IDs for users requiring notifications.
    payload (dict): Optional dictionary with custom attributes needed by the template.
    overrides (dict): Additional attributes needed for template integrations.

    """
    def __init__(
        self,
        id: str,
        subscribers: list[str] = None,
        payload: dict = None,
        overrides: dict = None
    ):
        self.id = id
        self.subscribers = subscribers
        self.payload = payload
        self.overrides = overrides


class Subscriber:
    """
    Class representing a Novu subscriber.

    Attributes:

    id (str): Unique ID of the subscriber.
    email (str): Optional email address for the subscriber.
    first_name (str): Optional first name of the subscriber.
    last_name (str): Optional last name of the subscriber.
    phone (str): Optional phone number of the subscriber.
    avatar (str): Optional URL pointing to a profile picture.

    """
    def __init__(
        self,
        id: str,
        email: str = None,
        first_name: str = None,
        last_name: str = None,
        phone: str = None,
        avatar: str = None,
    ):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.avatar = avatar
