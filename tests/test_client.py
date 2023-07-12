from unittest.mock import patch

import httpx
import pytest
from asyncnovu._utils import format
from asyncnovu.client import NovuClient
from asyncnovu.enums.provider import PushProviderIdEnum
from asyncnovu.models import Subscriber, Trigger


@pytest.mark.asyncio
async def test_format_util():
    # Testing format function.
    result = format(200, {"data": "data"})
    assert result == {
        "status_code": 200,
        "detail": "data",
    }

    result = format(404, {"statusCode": 404, "detail_1": "detail_1", "detail_2": "detail_2"})
    assert result == {
        "status_code": 404,
        "detail": {"detail_1": "detail_1", "detail_2": "detail_2"},
    }


@pytest.mark.asyncio
@patch("httpx.AsyncClient.delete")
@patch("httpx.AsyncClient.post")
async def test_event_actions(httpx_post_mock, httpx_delete_mock):
    # Creating Novu Client.
    client = NovuClient("api_key", "api_url")

    # Mocking httpx calls to Novu.
    httpx_post_mock.return_value = httpx.Response(
        200, json={"data": "Test passed."}, request=httpx.Request("POST", "test")
    )

    httpx_delete_mock.return_value = httpx.Response(
        200, json={"data": "Test passed."}, request=httpx.Request("DELETE", "test")
    )

    # Testing trigger function to send an event.
    response = await client.trigger_event(
        Trigger(
            id="trigger_id",
            subscribers=["subscriber_id"],
            payload={"data": "data"},
            overrides={"overrides": "overrides"}
        )
    )
    assert response == {"status_code": 200, "detail": "Test passed."}

    # Checking if correct inputs went into httpx call.
    assert httpx_post_mock.call_count == 1
    httpx_post_mock.assert_called_with(
        "api_url/events/trigger",
        json={
            "name": "trigger_id",
            "to": ["subscriber_id"],
            "payload": {"data": "data"},
            "overrides": {"overrides": "overrides"},
        },
        headers=client.headers,
    )

    # Testing bulk trigger function.
    response = await client.bulk_trigger(
        [
            Trigger(
                id="trigger_1",
                subscribers=["subscriber_1"],
                payload={"data_1": "data_1"},
                overrides={"overrides_1": "overrides_1"}
            ),
            Trigger(
                id="trigger_2",
                subscribers=["subscriber_2"],
                payload={"data_2": "data_2"},
                overrides={"overrides_2": "overrides_2"}
            ),
        ]
    )
    assert response == {"status_code": 200, "detail": "Test passed."}

    # Checking if correct inputs went into httpx call.
    assert httpx_post_mock.call_count == 2
    httpx_post_mock.assert_called_with(
        "api_url/events/trigger/bulk",
        json={
            "events": [
                {
                    "name": "trigger_1",
                    "to": ["subscriber_1"],
                    "payload": {"data_1": "data_1"},
                    "overrides": {"overrides_1": "overrides_1"},
                },
                {
                    "name": "trigger_2",
                    "to": ["subscriber_2"],
                    "payload": {"data_2": "data_2"},
                    "overrides": {"overrides_2": "overrides_2"},
                },
            ],
        },
        headers=client.headers,
    )

    # Testing function to broadcast an event.
    response = await client.broadcast_event(
        Trigger(
            id="trigger_id",
            payload={"data": "data"},
            overrides={"overrides": "overrides"},
        )
    )
    assert response == {"status_code": 200, "detail": "Test passed."}

    # Checking if correct inputs went into httpx call.
    assert httpx_post_mock.call_count == 3
    httpx_post_mock.assert_called_with(
        "api_url/events/trigger/broadcast",
        json={
            "name": "trigger_id",
            "payload": {"data": "data"},
            "overrides": {"overrides": "overrides"},
        },
        headers=client.headers,
    )

    # Testing function to cancel an event.
    response = await client.cancel_event("transaction_id")
    assert response == {"status_code": 200, "detail": "Test passed."}

    # Checking if correct inputs went into httpx call.
    assert httpx_delete_mock.call_count == 1
    httpx_delete_mock.assert_called_with(
        "api_url/events/trigger/transaction_id",
        headers=client.headers,
    )


@pytest.mark.asyncio
@patch("httpx.AsyncClient.delete")
@patch("httpx.AsyncClient.put")
@patch("httpx.AsyncClient.post")
@patch("httpx.AsyncClient.get")
async def test_subscriber_actions(httpx_get_mock, httpx_post_mock, httpx_put_mock, httpx_delete_mock):
    # Creating Novu Client.
    client = NovuClient("api_key", "api_url")

    # Mocking httpx calls to Novu.
    httpx_get_mock.return_value = httpx.Response(
        200, json={"data": "Test passed."}, request=httpx.Request("GET", "test")
    )

    httpx_post_mock.return_value = httpx.Response(
        200, json={"data": "Test passed."}, request=httpx.Request("POST", "test")
    )

    httpx_put_mock.return_value = httpx.Response(
        200, json={"data": "Test passed."}, request=httpx.Request("PUT", "test")
    )

    httpx_delete_mock.return_value = httpx.Response(
        200, json={"data": "Test passed."}, request=httpx.Request("DELETE", "test")
    )

    # Testing function to get a subscriber profile.
    response = await client.get_subscriber("subscriber_id")
    assert response == {"status_code": 200, "detail": "Test passed."}

    # Checking if correct inputs went into httpx call.
    assert httpx_get_mock.call_count == 1
    httpx_get_mock.assert_called_with(
        "api_url/subscribers/subscriber_id",
        headers=client.headers,
    )

    # Testing function to upsert a subscriber profile.
    response = await client.upsert_subscriber(
        Subscriber(
            id="subscriber_id",
            email="subscriber@gmail.com",
            first_name="Test",
            last_name="Subscriber",
        )
    )
    assert response == {"status_code": 200, "detail": "Test passed."}

    # Checking if correct inputs went into httpx call.
    assert httpx_post_mock.call_count == 1
    httpx_post_mock.assert_called_with(
        "api_url/subscribers",
        json={
            "subscriberId": "subscriber_id",
            "email": "subscriber@gmail.com",
            "firstName": "Test",
            "lastName": "Subscriber",
            "phone": None,
            "avatar": None,
        },
        headers=client.headers,
    )

    # Testing function to update subscriber credentials.
    response = await client.update_subscriber_credentials(
        "subscriber_id", PushProviderIdEnum.FCM, {"deviceTokens": ["token_1"]}
    )
    assert response == {"status_code": 200, "detail": "Test passed."}

    # Checking if correct inputs went into httpx call.
    assert httpx_put_mock.call_count == 1
    httpx_put_mock.assert_called_with(
        "api_url/subscribers/subscriber_id/credentials",
        json={
            "providerId": "fcm",
            "credentials": {
                "deviceTokens": ["token_1"],
            },
        },
        headers=client.headers,
    )

    # Testing function to delete a subscriber profile.
    response = await client.delete_subscriber("subscriber_id")
    assert response == {"status_code": 200, "detail": "Test passed."}

    # Checking if correct inputs went into httpx call.
    assert httpx_delete_mock.call_count == 1
    httpx_delete_mock.assert_called_with(
        "api_url/subscribers/subscriber_id",
        headers=client.headers,
    )
