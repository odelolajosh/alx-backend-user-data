#!/usr/bin/env python3
""" Filter Logger """
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """ Returns the log message obfuscated. """
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message
