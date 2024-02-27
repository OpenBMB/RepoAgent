import requests
from requests.exceptions import RequestException
from time import sleep
from repo_agent.exceptions import APIError
"""
OpenAIAPIClient 类将负责与OpenAI API的所有通信，包括发送请求和处理响应。它还将处理API调用的重试逻辑。
"""
class OpenAIAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def call_api(self, endpoint, payload, retries=3, backoff_factor=0.3):
        """
        Call the OpenAI API with the given endpoint and payload.
        Retries on failures with exponential backoff.

        Parameters:
            endpoint (str): The API endpoint to call.
            payload (dict): The payload to send in the API call.
            retries (int): Number of times to retry on failure.
            backoff_factor (float): Factor by which to increase delay between retries.

        Returns:
            dict: The JSON response from the API.

        Raises:
            APIError: An error occurred when calling the API.
        """
        for attempt in range(retries):
            try:
                response = requests.post(endpoint, json=payload, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except RequestException as e:
                if attempt < retries - 1:
                    sleep((2 ** attempt) * backoff_factor)
                    continue
                else:
                    raise APIError(e, status_code=response.status_code if response else None)
