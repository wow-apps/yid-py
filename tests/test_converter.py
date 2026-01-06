"""Tests for yid_py converter module."""

import pytest

import yid_py
from yid_py import (
    ConverterError,
    Encoder,
    Transform,
    create,
    to_alphanumeric,
    to_numeric,
)


class TestToAlphanumeric:
    """Tests for to_alphanumeric function."""

    def test_basic_conversion(self) -> None:
        """Test basic number to alphanumeric conversion."""
        assert to_alphanumeric(12345) == "dnh"

    def test_zero(self) -> None:
        """Test conversion of zero."""
        assert to_alphanumeric(0) == "a"

    def test_one(self) -> None:
        """Test conversion of one."""
        assert to_alphanumeric(1) == "b"

    def test_single_digit_boundary(self) -> None:
        """Test boundary of single character output."""
        assert to_alphanumeric(61) == "Z"
        assert to_alphanumeric(62) == "ba"

    def test_large_number(self) -> None:
        """Test conversion of large numbers."""
        result = to_alphanumeric(999999999)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_with_secure_key(self) -> None:
        """Test conversion with secure key."""
        result = to_alphanumeric(12345, secure_key="my-secret")
        assert result != to_alphanumeric(12345)
        assert isinstance(result, str)

    def test_different_secure_keys_produce_different_results(self) -> None:
        """Test that different secure keys produce different outputs."""
        result1 = to_alphanumeric(12345, secure_key="key1")
        result2 = to_alphanumeric(12345, secure_key="key2")
        assert result1 != result2

    def test_transform_upper(self) -> None:
        """Test uppercase transformation."""
        result = to_alphanumeric(12345, transform=Transform.UPPER)
        assert result == "DNH"
        assert result.isupper()

    def test_transform_lower(self) -> None:
        """Test lowercase transformation."""
        result = to_alphanumeric(12345, transform=Transform.LOWER)
        assert result == "dnh"
        assert result.islower()

    def test_transform_none(self) -> None:
        """Test no transformation."""
        result = to_alphanumeric(12345, transform=Transform.NONE)
        assert result == "dnh"

    def test_with_pad_up(self) -> None:
        """Test conversion with pad_up parameter."""
        result_no_pad = to_alphanumeric(1)
        result_with_pad = to_alphanumeric(1, pad_up=3)
        assert result_no_pad != result_with_pad

    def test_combined_options(self) -> None:
        """Test conversion with multiple options."""
        result = to_alphanumeric(
            12345,
            secure_key="secret",
            transform=Transform.UPPER
        )
        assert isinstance(result, str)
        assert result.isupper()


class TestToNumeric:
    """Tests for to_numeric function."""

    def test_basic_conversion(self) -> None:
        """Test basic alphanumeric to number conversion."""
        assert to_numeric("dnh") == 12345

    def test_zero_value(self) -> None:
        """Test conversion of 'a' back to zero."""
        assert to_numeric("a") == 0

    def test_one_value(self) -> None:
        """Test conversion of 'b' back to one."""
        assert to_numeric("b") == 1

    def test_boundary_values(self) -> None:
        """Test boundary values."""
        assert to_numeric("Z") == 61
        assert to_numeric("ba") == 62

    def test_with_secure_key(self) -> None:
        """Test conversion with secure key."""
        encoded = to_alphanumeric(12345, secure_key="my-secret")
        decoded = to_numeric(encoded, secure_key="my-secret")
        assert decoded == 12345

    def test_wrong_secure_key_produces_wrong_result(self) -> None:
        """Test that wrong secure key produces wrong result."""
        encoded = to_alphanumeric(12345, secure_key="correct-key")
        decoded = to_numeric(encoded, secure_key="wrong-key")
        assert decoded != 12345

    def test_with_pad_up(self) -> None:
        """Test conversion with pad_up parameter."""
        encoded = to_alphanumeric(100, pad_up=3)
        decoded = to_numeric(encoded, pad_up=3)
        assert decoded == 100

    def test_roundtrip(self) -> None:
        """Test encoding and decoding produces original value."""
        for num in [0, 1, 10, 100, 1000, 12345, 999999]:
            encoded = to_alphanumeric(num)
            decoded = to_numeric(encoded)
            assert decoded == num

    def test_roundtrip_with_secure_key(self) -> None:
        """Test roundtrip with secure key."""
        for num in [0, 1, 100, 12345, 999999]:
            encoded = to_alphanumeric(num, secure_key="test-key")
            decoded = to_numeric(encoded, secure_key="test-key")
            assert decoded == num


class TestTransformEnum:
    """Tests for Transform enum."""

    def test_enum_values_exist(self) -> None:
        """Test that all enum values exist."""
        assert Transform.NONE is not None
        assert Transform.UPPER is not None
        assert Transform.LOWER is not None

    def test_enum_values_are_unique(self) -> None:
        """Test that enum values are unique."""
        values = [Transform.NONE, Transform.UPPER, Transform.LOWER]
        assert len(values) == len(set(values))


class TestEncoder:
    """Tests for Encoder class."""

    def test_basic_encode(self) -> None:
        """Test basic encoding with Encoder."""
        enc = Encoder()
        assert enc.encode(12345) == "dnh"

    def test_basic_decode(self) -> None:
        """Test basic decoding with Encoder."""
        enc = Encoder()
        assert enc.decode("dnh") == 12345

    def test_encode_raw(self) -> None:
        """Test encode_raw method."""
        enc = Encoder(transform=Transform.UPPER)
        raw = enc.encode_raw(12345)
        display = enc.encode(12345)
        assert raw == "dnh"
        assert display == "DNH"

    def test_with_secure_key(self) -> None:
        """Test Encoder with secure key."""
        enc = Encoder(secure_key="secret")
        encoded = enc.encode(12345)
        decoded = enc.decode(encoded)
        assert decoded == 12345

    def test_with_transform(self) -> None:
        """Test Encoder with transform."""
        enc = Encoder(transform=Transform.UPPER)
        result = enc.encode(12345)
        assert result.isupper()

    def test_with_pad_up(self) -> None:
        """Test Encoder with pad_up."""
        enc = Encoder(pad_up=3)
        encoded = enc.encode(100)
        decoded = enc.decode(encoded)
        assert decoded == 100

    def test_roundtrip(self) -> None:
        """Test Encoder roundtrip."""
        enc = Encoder(secure_key="test", pad_up=2)
        for num in [0, 1, 100, 12345]:
            raw = enc.encode_raw(num)
            decoded = enc.decode(raw)
            assert decoded == num

    def test_multiple_encoders_independence(self) -> None:
        """Test that multiple encoders work independently."""
        enc1 = Encoder(secure_key="key1")
        enc2 = Encoder(secure_key="key2")
        assert enc1.encode(12345) != enc2.encode(12345)


class TestCreateFactory:
    """Tests for create factory function."""

    def test_create_returns_encoder(self) -> None:
        """Test that create returns an Encoder instance."""
        enc = create()
        assert isinstance(enc, Encoder)

    def test_create_with_options(self) -> None:
        """Test create with options."""
        enc = create(secure_key="secret", transform=Transform.UPPER, pad_up=2)
        result = enc.encode(12345)
        assert isinstance(result, str)
        assert result.isupper()

    def test_create_equivalent_to_encoder(self) -> None:
        """Test that create produces same results as Encoder constructor."""
        enc1 = create(secure_key="test")
        enc2 = Encoder(secure_key="test")
        assert enc1.encode(12345) == enc2.encode(12345)


class TestConverterError:
    """Tests for ConverterError exception."""

    def test_error_is_value_error(self) -> None:
        """Test that ConverterError inherits from ValueError."""
        assert issubclass(ConverterError, ValueError)

    def test_error_can_be_raised(self) -> None:
        """Test that ConverterError can be raised and caught."""
        with pytest.raises(ConverterError):
            raise ConverterError("test error")

    def test_error_message(self) -> None:
        """Test ConverterError message."""
        try:
            raise ConverterError("custom message")
        except ConverterError as e:
            assert str(e) == "custom message"


class TestModuleExports:
    """Tests for module-level exports."""

    def test_version_exists(self) -> None:
        """Test that __version__ is defined."""
        assert hasattr(yid_py, "__version__")
        assert isinstance(yid_py.__version__, str)

    def test_all_exports_accessible(self) -> None:
        """Test that all expected exports are accessible."""
        assert hasattr(yid_py, "to_alphanumeric")
        assert hasattr(yid_py, "to_numeric")
        assert hasattr(yid_py, "Transform")
        assert hasattr(yid_py, "Encoder")
        assert hasattr(yid_py, "create")
        assert hasattr(yid_py, "ConverterError")


class TestPrivateFunctions:
    """Tests for private functions to achieve full coverage."""

    def test_apply_transform_invalid_type(self) -> None:
        """Test _apply_transform with invalid transform type."""
        from yid_py.converter import _apply_transform

        with pytest.raises(ConverterError, match="Invalid transform type"):
            _apply_transform("test", "invalid")  # type: ignore[arg-type]


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_very_large_number(self) -> None:
        """Test with very large numbers."""
        large_num = 10**15
        encoded = to_alphanumeric(large_num)
        decoded = to_numeric(encoded)
        assert decoded == large_num

    def test_empty_secure_key_treated_as_none(self) -> None:
        """Test that empty string secure key works like None."""
        result_none = to_alphanumeric(12345, secure_key=None)
        result_empty = to_alphanumeric(12345, secure_key="")
        # Empty string is falsy, so should be same as None
        assert result_none == result_empty

    def test_special_characters_in_secure_key(self) -> None:
        """Test secure key with special characters."""
        encoded = to_alphanumeric(12345, secure_key="!@#$%^&*()")
        decoded = to_numeric(encoded, secure_key="!@#$%^&*()")
        assert decoded == 12345

    def test_unicode_secure_key(self) -> None:
        """Test secure key with unicode characters."""
        encoded = to_alphanumeric(12345, secure_key="ключ")
        decoded = to_numeric(encoded, secure_key="ключ")
        assert decoded == 12345

    def test_long_secure_key(self) -> None:
        """Test with very long secure key."""
        long_key = "a" * 1000
        encoded = to_alphanumeric(12345, secure_key=long_key)
        decoded = to_numeric(encoded, secure_key=long_key)
        assert decoded == 12345

    def test_consecutive_numbers(self) -> None:
        """Test that consecutive numbers produce different outputs."""
        results = [to_alphanumeric(i) for i in range(100)]
        assert len(results) == len(set(results))

    def test_pad_up_zero(self) -> None:
        """Test pad_up with zero value."""
        result = to_alphanumeric(12345, pad_up=0)
        assert result == "dnh"

    def test_pad_up_one(self) -> None:
        """Test pad_up with one (should be same as zero)."""
        result_0 = to_alphanumeric(12345, pad_up=0)
        result_1 = to_alphanumeric(12345, pad_up=1)
        assert result_0 == result_1

    def test_dictionary_characters(self) -> None:
        """Test that output only contains valid dictionary characters."""
        import string
        valid_chars = set(string.ascii_lowercase + string.digits + string.ascii_uppercase)

        for num in [0, 1, 62, 100, 12345, 999999]:
            result = to_alphanumeric(num)
            assert all(c in valid_chars for c in result)
