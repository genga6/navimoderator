import httpx
import pytest


BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.asyncio
async def test_moderate_full_workflow():
    payload = {
        "streamer_login": "test_streamer_login", 
        "access_token": "test_access_token", 
        "refresh_token": "test_refresh_token", 
        "comments": [
            {
                "timestamp": "2025-03-14T12:34:56Z",
                "user_name": "someone_in_chat",
                "comment_id": "abcd1234",
                "comment": "こんにちは！"
            },
            {
                "timestamp": "2025-03-14T12:34:56Z",
                "user_name": "someone_in_chat",
                "comment_id": "abcd1234",
                "comment": "Hello!"
            }
        ],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/moderate", json=payload)

        assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response: {response.text}"

        json_response = response.json()
        assert "comments" in json_response, "Missing key `comments` in response"
        
        processed_comments = json_response["comments"]
        assert isinstance(processed_comments, list), f"`processed_comments` should be a list, got {type(processed_comments)}"

        print(f"Full workflow response: {json_response}")


@pytest.mark.asyncio
async def test_moderate_partial_workflow():
    payload = {
        "streamer_login": "test",
        "access_token": "test",
        "refresh_token": "test",
        "user_name": "test",
        "comments": [
            {
            "timestamp": "2025-03-14T12:34:56Z", 
            "user_name": "@someone_in_chat", 
            "comment_id": "abcd5678", 
            "comment": "Hello!", 
            "translated_text": "こんにちは!",
	        "is_harassment": False,  
            }, 
            {
            "timestamp": "2025-03-14T12:34:56Z", 
            "user_name": "@someone_in_chat", 
            "comment_id": "abcd5678", 
            "comment": "これは誹謗中傷コメントです。" , 
            "translated_text": "",
	        "is_harassment": True,  
            }, 
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/moderate", json=payload)

        assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response: {response.text}"

        json_response = response.json()
        assert "comments" in json_response, "Missing key 'comments' in response"

        processed_comments = json_response["comments"]
        assert isinstance(processed_comments, list), f"'processed_comments' should be a list, got {type(processed_comments)}"

        print(f"Partial workflow response: {json_response}")
