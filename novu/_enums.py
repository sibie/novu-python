from enum import Enum

class PushIntegrations(str, Enum):
    """Collection of Provider IDs for working with Push integrations."""

    APN = "apn"
    EXPO = "expo"
    FCM = "fcm"