import httpx
import pytest


@pytest.mark.asyncio
async def test_moderate():
    url = "http://localhost:8000/moderate"

    payload = {
        "timestamp": "2025-03-14T12:34:56Z",
        "user_name": "someone_in_chat",
        "comment_id": "abcd1234",
        "comment": "Hello!"
    },
    {
        "timestamp": "2025-03-14T12:34:56Z",
        "user_name": "someone_in_chat",
        "comment_id": "abcd1234",
        "comment": "Hello!"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")