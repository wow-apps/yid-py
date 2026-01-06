# YouTubeID for Python

Generate YouTube-style short IDs from numbers. Lightweight, fast, and reversible base62 encoder with optional obfuscation.

[![PyPI version](https://badge.fury.io/py/yid.svg)](https://badge.fury.io/py/yid)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](https://github.com/wow-apps/yid-py)

## Other programming languages

- **PHP**: [kvz/youtube-id](https://github.com/kvz/youtube-id)
- **Python**: [wow-apps/yid-py](https://github.com/wow-apps/yid-py/)
- **TypeScript**: [wow-apps/yid-ts](https://github.com/wow-apps/yid-ts/)
- **Go Lang**: [wow-apps/yid-go](https://github.com/wow-apps/yid-go/)

## Features

- **Lightweight** - Zero dependencies, pure Python
- **Fast** - Simple base62 encoding/decoding
- **Reversible** - Encode and decode without data loss
- **Obfuscation** - Optional secure key to shuffle the dictionary
- **Type-safe** - Full type hints for IDE support

## Installation

```bash
pip install yid
```

Or with Poetry:

```bash
poetry add yid
```

## Quick Start

```python
import yid_py

# Encode a number to a short string
yid_py.to_alphanumeric(12345)  # -> 'dnh'

# Decode back to number
yid_py.to_numeric('dnh')  # -> 12345
```

## Usage

### Basic Encoding/Decoding

```python
import yid_py

# Number to alphanumeric
yid_py.to_alphanumeric(0)        # -> 'a'
yid_py.to_alphanumeric(61)       # -> 'Z'
yid_py.to_alphanumeric(62)       # -> 'ba'
yid_py.to_alphanumeric(12345)    # -> 'dnh'
yid_py.to_alphanumeric(999999)   # -> 'eGGf'

# Alphanumeric to number
yid_py.to_numeric('dnh')         # -> 12345
```

### With Secure Key (Obfuscation)

Use a secure key to shuffle the dictionary, making IDs harder to predict:

```python
import yid_py

# Without key
yid_py.to_alphanumeric(12345)                      # -> 'dnh'

# With secure key (different output)
yid_py.to_alphanumeric(12345, secure_key='secret') # -> 'UDJ'

# Decode with the same key
yid_py.to_numeric('UDJ', secure_key='secret')      # -> 12345
```

### Case Transformation

```python
from yid_py import to_alphanumeric, Transform

to_alphanumeric(12345, transform=Transform.UPPER)  # -> 'DNH'
to_alphanumeric(12345, transform=Transform.LOWER)  # -> 'dnh'
```

### Encoder Factory

For repeated operations with the same settings, use the `Encoder` class:

```python
import yid_py

# Create encoder with preset options
enc = yid_py.create(secure_key='my-secret', transform=yid_py.Transform.UPPER)

# Encode
enc.encode(12345)      # -> 'HQJ' (transformed for display)
enc.encode_raw(12345)  # -> 'hqj' (raw for storage/decoding)

# Decode
enc.decode('hqj')      # -> 12345
```

## API Reference

### Functions

#### `to_alphanumeric(number, pad_up=0, secure_key=None, transform=Transform.NONE)`

Convert a number to a short alphanumeric string.

| Parameter    | Type          | Default  | Description               |
|--------------|---------------|----------|---------------------------|
| `number`     | `int`         | required | The number to convert     |
| `pad_up`     | `int`         | `0`      | Padding value             |
| `secure_key` | `str \| None` | `None`   | Key to shuffle dictionary |
| `transform`  | `Transform`   | `NONE`   | Case transformation       |

#### `to_numeric(alphanumeric, pad_up=0, secure_key=None)`

Convert an alphanumeric string back to a number.

| Parameter      | Type          | Default  | Description                         |
|----------------|---------------|----------|-------------------------------------|
| `alphanumeric` | `str`         | required | The string to convert               |
| `pad_up`       | `int`         | `0`      | Padding value (must match encoding) |
| `secure_key`   | `str \| None` | `None`   | Key (must match encoding)           |

#### `create(pad_up=0, secure_key=None, transform=Transform.NONE)`

Create a reusable `Encoder` instance with preset options.

### Classes

#### `Encoder`

Reusable encoder with preset options.

- `encode(number)` - Convert number to alphanumeric (with transform)
- `encode_raw(number)` - Convert number to alphanumeric (without transform)
- `decode(alphanumeric)` - Convert alphanumeric to number

#### `Transform`

Enum for case transformation:

- `Transform.NONE` - No transformation
- `Transform.UPPER` - Uppercase output
- `Transform.LOWER` - Lowercase output

## Use Cases

- **URL shorteners** - Convert database IDs to short URLs
- **Public IDs** - Hide sequential database IDs from users
- **Share codes** - Generate readable codes for sharing
- **Invite links** - Create short invitation tokens

## Performance

The library uses base62 encoding (a-z, 0-9, A-Z) which provides:

| Number Range         | Output Length |
|----------------------|---------------|
| 0 - 61               | 1 character   |
| 62 - 3,843           | 2 characters  |
| 3,844 - 238,327      | 3 characters  |
| 238,328 - 14,776,335 | 4 characters  |

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

```bash
# Clone and setup
git clone https://github.com/wow-apps/yid-py.git
cd yid-py
python3.10 -m venv venv
source venv/bin/activate
poetry install --with dev

# Run tests
pytest --cov=yid_py
```

## Credits

A Python port of the YouTube-style ID generator originally created by [Kevin van Zonneveld](https://github.com/kvz) and contributors.

## License

[MIT](LICENSE) © Oleksii Samara, Kevin van Zonneveld
