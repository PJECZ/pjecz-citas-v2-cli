"""
CLI Enc Sistemas Request API
"""
from datetime import date
from typing import Any

import requests

from common.exceptions import CLIConnectionError, CLIResponseError, CLIStatusCodeError
from config.settings import BASE_URL, LIMIT, TIMEOUT
