#!/usr/bin/env python3
"""Token-usage capture on the Anthropic API client used by the false-positive filter."""

from types import SimpleNamespace
from unittest.mock import Mock, patch

from claudecode.claude_api_client import ClaudeAPIClient


def _response(text='{"is_false_positive": false}', **usage):
    return SimpleNamespace(content=[SimpleNamespace(text=text)], usage=SimpleNamespace(**usage))


@patch('claudecode.claude_api_client.Anthropic')
def test_call_with_retry_accumulates_usage(mock_anthropic):
    client = ClaudeAPIClient(model='claude-test', api_key='k')
    mock_anthropic.return_value.messages.create.side_effect = [
        _response(input_tokens=120, output_tokens=30, cache_creation_input_tokens=0, cache_read_input_tokens=100),
        _response(input_tokens=80, output_tokens=20),
    ]
    ok, text, err = client.call_with_retry('p')
    assert ok and err == ''
    ok, _, _ = client.call_with_retry('q')
    assert ok
    assert client.usage == {
        'calls': 2, 'input_tokens': 200, 'output_tokens': 50,
        'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 100,
    }


@patch('claudecode.claude_api_client.Anthropic')
def test_response_without_usage_is_not_counted(mock_anthropic):
    client = ClaudeAPIClient(model='claude-test', api_key='k')
    mock_anthropic.return_value.messages.create.return_value = SimpleNamespace(content=[SimpleNamespace(text='x')])
    ok, _, _ = client.call_with_retry('p')
    assert ok
    assert client.usage['calls'] == 0
