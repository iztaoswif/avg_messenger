import pytest

from app.core.config import MAX_TEXT_LENGTH
from app.chat.schemas import validate_message_text
from app.chat.exceptions import InappropriateMessageTextError


def test_removed_zw_from_message_text():
    zw_characters = "\u200b\u200c\u200d\u2060\ufeff"
    #invisible (zero-width) characters
    assert len(zw_characters) == 5

    expected_validation = {
        "hel" + zw_characters[0] + "lo": "hello",
        "f" + zw_characters[1] + "rom": "from",
        "the" + zw_characters[2]: "the",
        zw_characters[3] + "test": "test",
        "sui" + zw_characters[4] + "te": "suite",
        "just to" + ''.join(zw_characters) + " be sure": "just to be sure"
    }
    
    for unvalidated, validated in expected_validation.items():
        assert validate_message_text(unvalidated) == validated


def test_disallow_exceedingly_long_messages():
    with pytest.raises(InappropriateMessageTextError) as text_error:
        validate_message_text("h" * (MAX_TEXT_LENGTH + 1))
    assert "must be at most" in str(text_error.value)

    valid_long_text = 'h' * MAX_TEXT_LENGTH
    assert(validate_message_text(valid_long_text) == valid_long_text)


def test_disallow_empty_messages():
    empty_messages = [
        " ",
        "    ",
        "   "
    ]

    for message in empty_messages:
        with pytest.raises(InappropriateMessageTextError) as text_error:
            validate_message_text(message)
        assert "is empty" in str(text_error.value)


def test_disallow_invalid_messages():
    invalid_messages = [
        "\u200b\u200c",
        "   \ufeff"
    ]

    for message in invalid_messages:
        with pytest.raises(InappropriateMessageTextError) as text_error:
            validate_message_text(message)
        assert "has no valid characters" in str(text_error.value)


def test_disallow_zero_length_messages():
    with pytest.raises(InappropriateMessageTextError) as text_error:
        validate_message_text("")
    assert "must be at least" in str(text_error.value)
