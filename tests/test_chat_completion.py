import pytest
import openai

# 模拟的OpenAI类
class MockOpenAI:
    class Chat:
        def __init__(self, api_key):
            self.api_key = api_key
            self.completions = self.Completions()

        class Completions:
            @staticmethod
            def create(*args, **kwargs):
                return {
                    "choices": [{
                        "message": {
                            "role": "assistant",
                            "content": "This is a mock response for testing."
                        }
                    }]
                }

    def __init__(self, api_key):
        self.chat = MockOpenAI.Chat(api_key)

@pytest.fixture
def mock_openai(monkeypatch):
    # 替换 openai.OpenAI 类为模拟的版本
    monkeypatch.setattr(openai, 'OpenAI', MockOpenAI)

    # 返回一个模拟的OpenAI客户端实例
    return MockOpenAI(api_key="fake-key")

def test_chat_completion(mock_openai):
    # 使用fixture提供的模拟客户端
    client = mock_openai

    # 调用 completions.create 方法
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say this is a test"}]
    )

    # 验证返回的模拟数据是否正确
    assert chat_completion['choices'][0]['message']['content'] == "This is a mock response for testing."
