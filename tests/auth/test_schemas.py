import pytest

from app.core.config import MAX_USERNAME_LENGTH, MAX_PASSWORD_LENGTH
from app.auth.schemas import validate_username, validate_password
from app.auth.exceptions import InappropriateUsernameError, InappropriatePasswordError


#-------------------------------
#username related tests

def test_disallow_zw_characters_in_username():
    zw_characters = "\u200b\u200c\u200d\u2060\ufeff"
    #invisible (zero-width) characters
    assert len(zw_characters) == 5

    invalid_usernames = [
        zw_characters[0],
        "str" + zw_characters[1] + "ing",
        "michael" + zw_characters[2],
        zw_characters[3],
        zw_characters[4]
    ]

    for invalid_username in invalid_usernames:
        with pytest.raises(InappropriateUsernameError) as username_error:
            validate_username(invalid_username)
        assert "Invalid character" in str(username_error.value)


def test_disallow_long_usernames():
    invalid_usernames = [
        'd' * (MAX_USERNAME_LENGTH + 1),
        'c' * (MAX_USERNAME_LENGTH + 2)
    ]

    for invalid_username in invalid_usernames:
        with pytest.raises(InappropriateUsernameError) as username_error:
            validate_username(invalid_username)
        assert("at most" in str(username_error.value))


def test_disallow_empty_usernames():
    invalid_usernames = [
        "  ",
        "        ",
        "      "
    ]

    for invalid_username in invalid_usernames:
        with pytest.raises(InappropriateUsernameError) as username_error:
            validate_username(invalid_username)
        assert("empty" in str(username_error.value))


def test_disallow_zero_length_usernames():
    with pytest.raises(InappropriateUsernameError) as username_error:
        validate_username("")
    assert("at least" in str(username_error.value))


def test_allow_valid_usernames():
    valid_usernames = [
        "%18(3)",
        "  Michael12&",
        " Иван 91#$! ",
        "a ",
        "aw@#電車魚愛12`",
        'c' * MAX_USERNAME_LENGTH,
        "ßßÄÄ"
    ]

    for valid_username in valid_usernames:
        assert(validate_username(valid_username)) == valid_username.strip()


#-------------------------------
#password related tests


def test_disallow_short_passwords():
    invalid_passwords = [
        "",
        "a",
        "v4",
        "7&m",
        "0asz",
        "7dnZp",
        "123456",
        "pIxohje"
    ]

    for invalid_password in invalid_passwords:
        with pytest.raises(InappropriatePasswordError) as password_error:
            validate_password(invalid_password)
        assert("at least 8" in str(password_error.value))


def test_disallow_long_passwords():
    invalid_passwords = [
        'a' * (MAX_PASSWORD_LENGTH + 1),
        'cdsfsfsd' * 999
    ]

    for invalid_password in invalid_passwords:
        with pytest.raises(InappropriatePasswordError) as password_error:
            validate_password(invalid_password)
        assert("at most" in str(password_error.value))


def test_disallow_invalid_characters_in_passwords():
    invalid_passwords = [
        "12345雫雫夢",
        "😫😫🚴✔️😫😫😫😫",
        "m̷̥̃y̷̹͋̏ ̴̲͆͝p̴̗͇̈́̍a̶̟͍̔̓s̸̜̎̓s̵̜̩͒͘ẅ̷̤̃o̶͓̒̆r̴̛͚̓d̵̲̃",
        "m̷y̵ ̷p̶a̸s̶s̸w̸o̷r̷d̸",
        "\u200b\u200b\u200b\u200b\u200b\u200b\u200b\u200b",
        "\n\n\n\n\n\n\n\n",
        "\t\t\t\t\t\t\t\t"
    ]

    for invalid_password in invalid_passwords:
        with pytest.raises(InappropriatePasswordError) as password_error:
            validate_password(invalid_password)
        assert("Invalid character" in str(password_error.value))
