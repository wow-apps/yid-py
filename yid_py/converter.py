"""
Generate YouTube-style short IDs from numbers.
Lightweight, fast, and reversible base62 encoder with optional obfuscation.

Authors:
    Oleksii Samara <oleksii@wildsoft.io> (https://github.com/wow-apps)
    Kevin van Zonneveld <kevin@transloadit.com> (https://github.com/kvz)
"""

import hashlib
import math
import string
from enum import Enum, auto


class ConverterError(ValueError):
    """Raised when conversion fails."""

    pass


class Transform(Enum):
    """Transformation options for alphanumeric output."""

    NONE = auto()
    UPPER = auto()
    LOWER = auto()


# Base dictionary: a-z + 0-9 + A-Z (62 characters)
_DICTIONARY = string.ascii_lowercase + string.digits + string.ascii_uppercase
_DICT_LEN = len(_DICTIONARY)


def to_alphanumeric(
    number: int,
    pad_up: int = 0,
    secure_key: str | None = None,
    transform: Transform = Transform.NONE,
) -> str:
    """
    Convert a number to a short alphanumeric string.

    Args:
        number: The number to convert.
        pad_up: Padding value for the conversion.
        secure_key: Optional key to shuffle the dictionary.
        transform: Case transformation (NONE, UPPER, LOWER).

    Returns:
        The alphanumeric string.

    Example:
        >>> to_alphanumeric(12345)
        'dnh'
        >>> to_alphanumeric(12345, transform=Transform.UPPER)
        'DNH'
    """
    dictionary = _secure_dictionary(secure_key) if secure_key else _DICTIONARY
    result = _num_to_alpha(number, dictionary, pad_up)
    return _apply_transform(result, transform)


def to_numeric(
    alphanumeric: str, pad_up: int = 0, secure_key: str | None = None
) -> int:
    """
    Convert an alphanumeric string back to a number.

    Args:
        alphanumeric: The alphanumeric string to convert.
        pad_up: Padding value (must match the value used for encoding).
        secure_key: Optional key (must match the key used for encoding).

    Returns:
        The numeric value.

    Example:
        >>> to_numeric('dnh')
        12345
    """
    dictionary = _secure_dictionary(secure_key) if secure_key else _DICTIONARY
    return _alpha_to_num(alphanumeric, dictionary, pad_up)


class Encoder:
    """
    Reusable encoder with preset options.

    Example:
        >>> enc = Encoder(secure_key="secret", transform=Transform.UPPER)
        >>> enc.encode(12345)
        'HQJ'
        >>> enc.decode('HQJ')
        12345
    """

    def __init__(
        self,
        pad_up: int = 0,
        secure_key: str | None = None,
        transform: Transform = Transform.NONE,
    ):
        self._pad_up = pad_up
        self._secure_key = secure_key
        self._transform = transform
        self._dictionary = _secure_dictionary(secure_key) if secure_key else _DICTIONARY

    def encode(self, number: int) -> str:
        """
        Convert a number to an alphanumeric string.

        Returns the transformed result (if transform was set).
        For the raw (non-transformed) result, use encode_raw().
        """
        result = _num_to_alpha(number, self._dictionary, self._pad_up)
        return _apply_transform(result, self._transform)

    def encode_raw(self, number: int) -> str:
        """Convert a number to an alphanumeric string without transform."""
        return _num_to_alpha(number, self._dictionary, self._pad_up)

    def decode(self, alphanumeric: str) -> int:
        """
        Convert an alphanumeric string back to a number.

        Expects the raw (non-transformed) value from encode_raw().
        """
        return _alpha_to_num(alphanumeric, self._dictionary, self._pad_up)


def create(
    pad_up: int = 0,
    secure_key: str | None = None,
    transform: Transform = Transform.NONE,
) -> Encoder:
    """
    Create a reusable encoder with preset options.

    Args:
        pad_up: Padding value for conversions.
        secure_key: Optional key to shuffle the dictionary.
        transform: Case transformation for encoding output.

    Returns:
        An Encoder instance.

    Example:
        >>> enc = create(secure_key="my-secret", transform=Transform.UPPER)
        >>> enc.encode(12345)
        'HQJ'
    """
    return Encoder(pad_up=pad_up, secure_key=secure_key, transform=transform)


# --- Private functions ---


def _secure_dictionary(secure_key: str) -> str:
    """
    Shuffle the dictionary based on a secure key.

    This makes it harder to calculate the corresponding numeric ID
    without knowing the key.
    """
    sha256_hash = hashlib.sha256(secure_key.encode()).hexdigest()
    secure_hash = (
        hashlib.sha512(secure_key.encode()).hexdigest()
        if len(sha256_hash) < _DICT_LEN
        else sha256_hash
    )

    paired = sorted(
        zip(secure_hash[:_DICT_LEN], _DICTIONARY, strict=True),
        key=lambda x: x[0],
        reverse=True,
    )

    return "".join(char for _, char in paired)


def _num_to_alpha(number: int, dictionary: str, pad_up: int = 0) -> str:
    """Convert number to alphanumeric string."""
    if pad_up > 1:
        number += _DICT_LEN ** (pad_up - 1)

    if number == 0:
        return dictionary[0]

    output = []
    t = int(math.log(number, _DICT_LEN))

    while t >= 0:
        bcp = _DICT_LEN ** t
        index = (number // bcp) % _DICT_LEN
        output.append(dictionary[index])
        number -= index * bcp
        t -= 1

    return "".join(output)


def _alpha_to_num(alphanumeric: str, dictionary: str, pad_up: int = 0) -> int:
    """Convert alphanumeric string to number."""
    result = 0

    for i, char in enumerate(reversed(alphanumeric)):
        result += dictionary.index(char) * (_DICT_LEN**i)

    if pad_up > 1:
        result -= _DICT_LEN ** (pad_up - 1)

    return result


def _apply_transform(value: str, transform: Transform) -> str:
    """Apply case transformation."""
    match transform:
        case Transform.NONE:
            return value
        case Transform.UPPER:
            return value.upper()
        case Transform.LOWER:
            return value.lower()
        case _:
            raise ConverterError(f"Invalid transform type: {transform}")
