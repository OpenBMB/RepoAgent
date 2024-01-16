import pytest
from click.testing import CliRunner
from repo_agent.main import cli, language_prompt  # Replace with your actual module name
from iso639 import LanguageNotFoundError

runner = CliRunner()

@pytest.fixture
def mock_language_prompt(mocker):
    return mocker.patch('language_prompt')  # Replace 'your_module' with the actual name of your module

def test_valid_input(mock_language_prompt):
    mock_language_prompt.return_value = 'en'
    result = runner.invoke(cli, ['configure'], input='en\n')
    assert 'Language selected: English (en)' in result.output
    assert result.exit_code == 0

def test_invalid_input_then_valid(mock_language_prompt):
    mock_language_prompt.side_effect = [LanguageNotFoundError, 'en']
    result = runner.invoke(cli, ['configure'], input='invalid\nen\n')
    assert 'Invalid language input. Please enter a valid ISO 639 code or language name.' in result.output
    assert result.exit_code == 0

def test_three_invalid_attempts(mock_language_prompt):
    mock_language_prompt.side_effect = [LanguageNotFoundError, LanguageNotFoundError, LanguageNotFoundError]
    result = runner.invoke(cli, ['configure'], input='invalid1\ninvalid2\ninvalid3\n')
    assert 'Failed to find the language after several attempts.' in result.output
    assert result.exit_code != 0
