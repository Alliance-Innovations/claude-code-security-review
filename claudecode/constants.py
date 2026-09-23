"""
Constants and configuration values for ClaudeCode.
"""

import os
import sys

# API Configuration
DEFAULT_CLAUDE_MODEL = os.environ.get('CLAUDE_MODEL') or 'claude-opus-5-5'
# Explicit: Opus 5.5 defaults to 'medium' when no effort is sent. The CLI
# answers an unknown --effort with a stderr warning and uses that default, so a
# typo would silently lower scan depth; fall back to 'high' loudly instead.
CLAUDE_EFFORTS = ('low', 'medium', 'high', 'xhigh', 'max')
DEFAULT_CLAUDE_EFFORT = (os.environ.get('CLAUDE_EFFORT') or 'high').strip().lower()
if DEFAULT_CLAUDE_EFFORT not in CLAUDE_EFFORTS:
    print(f"[Warning] CLAUDE_EFFORT={DEFAULT_CLAUDE_EFFORT!r} is not one of {CLAUDE_EFFORTS}; using 'high'", file=sys.stderr)
    DEFAULT_CLAUDE_EFFORT = 'high'
DEFAULT_TIMEOUT_SECONDS = 180  # 3 minutes
DEFAULT_MAX_RETRIES = 3
RATE_LIMIT_BACKOFF_MAX = 30  # Maximum backoff time for rate limits

# Token Limits
PROMPT_TOKEN_LIMIT = 16384  # 16k tokens max for claude-opus-4

# Exit Codes
EXIT_SUCCESS = 0
EXIT_GENERAL_ERROR = 1
EXIT_CONFIGURATION_ERROR = 2

# Subprocess Configuration
SUBPROCESS_TIMEOUT = 1200  # 20 minutes for Claude Code execution

