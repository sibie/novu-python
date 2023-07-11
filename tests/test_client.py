from unittest.mock import patch

import httpx
import pytest
from novu._utils import format
from novu.client import NovuClient


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
        "trigger_id", ["subscriber_id"], {"data": "data"}, {"overrides": "overrides"}
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

    # Testing function to broadcast an event.
    response = await client.broadcast_event(
        "trigger_id", {"data": "data"}, {"overrides": "overrides"}
    )
    assert response == {"status_code": 200, "detail": "Test passed."}

    # Checking if correct inputs went into httpx call.
    assert httpx_post_mock.call_count == 2
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
@patch("httpx.AsyncClient.post")
async def test_subscriber_actions(httpx_post_mock, httpx_delete_mock):
    # Creating Novu Client.
    client = NovuClient("api_key", "api_url")

    # Mocking httpx calls to Novu.
    httpx_post_mock.return_value = httpx.Response(
        200, json={"data": "Test passed."}, request=httpx.Request("POST", "test")
    )

    httpx_delete_mock.return_value = httpx.Response(
        200, json={"data": "Test passed."}, request=httpx.Request("DELETE", "test")
    )

    # Testing function to upsert a subscriber profile.
    response = await client.upsert_subscriber(
        "subscriber_id", "subscriber@cbamz.com", "Test", "Subscriber"
    )
    assert response == {"status_code": 200, "detail": "Test passed."}

    # Checking if correct inputs went into httpx call.
    assert httpx_post_mock.call_count == 1
    httpx_post_mock.assert_called_with(
        "api_url/subscribers",
        json={
            "subscriberId": "subscriber_id",
            "email": "subscriber@cbamz.com",
            "firstName": "Test",
            "lastName": "Subscriber",
            "phone": None,
            "avatar": None,
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
