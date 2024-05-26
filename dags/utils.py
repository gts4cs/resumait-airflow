from __future__ import annotations

import re


def check_content_question(text):
    """
    Check if wheteher it is question or not

    Parameters:
        question data (str)

    Return :
        bool data of checking question(bool)
    """

    pattern = r"자유형식|자유 형식|자유 양식|자유양식|0\d*\.\d*|\d+\.|(\(\d+\))|\d+\)"
    return bool(re.search(pattern, text))
