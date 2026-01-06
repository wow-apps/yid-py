"""
yid: Generate YouTube-style short IDs from numbers.
Lightweight, fast, and reversible base62 encoder with optional obfuscation.

Authors:
    Oleksii Samara <oleksii@wildsoft.io> (https://github.com/wow-apps)
    Kevin van Zonneveld <kevin@transloadit.com> (https://github.com/kvz)

Example:
    >>> import yid_py
    >>> yid_py.to_alphanumeric(12345)
    'dnh'
    >>> yid_py.to_numeric('dnh')
    12345

    # With secure key
    >>> yid_py.to_alphanumeric(12345, secure_key="secret")
    'hqj'

    # Using encoder factory
    >>> enc = yid_py.create(secure_key="secret", transform=yid_py.Transform.UPPER)
    >>> enc.encode(12345)
    'HQJ'
"""

from .converter import (
    ConverterError,
    Encoder,
    Transform,
    create,
    to_alphanumeric,
    to_numeric,
)

__all__ = [
    "to_alphanumeric",
    "to_numeric",
    "create",
    "Encoder",
    "Transform",
    "ConverterError",
]
__version__ = "1.0.0"
