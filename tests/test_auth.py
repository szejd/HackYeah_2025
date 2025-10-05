"""Unit tests for authentication utilities."""

from datetime import timedelta, datetime, timezone
import pytest
from fastapi import HTTPException
import jwt

from app.utils.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM


class TestPasswordHashing:
    """Test cases for password hashing functionality."""

    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string."""
        password = "test_password123"
        hashed = hash_password(password)

        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_different_hashes(self):
        """Test that same password generates different hashes (due to salt)."""
        password = "same_password"
        hash1 = hash_password(password)
        hash2 = hash_password(password)

        assert hash1 != hash2

    def test_hash_password_empty_string(self):
        """Test hashing an empty password."""
        hashed = hash_password("")

        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_special_characters(self):
        """Test hashing password with special characters."""
        password = "p@$$w0rd!#%&*()[]{}|;:',.<>?/~`"
        hashed = hash_password(password)

        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hash_password_unicode_characters(self):
        """Test hashing password with unicode characters."""
        password = "пароль密码🔒"
        hashed = hash_password(password)

        assert isinstance(hashed, str)
        assert len(hashed) > 0


class TestPasswordVerification:
    """Test cases for password verification functionality."""

    def test_verify_password_correct(self):
        """Test verifying correct password."""
        password = "correct_password"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test verifying incorrect password."""
        password = "correct_password"
        hashed = hash_password(password)

        assert verify_password("wrong_password", hashed) is False

    def test_verify_password_empty_password(self):
        """Test verifying empty password."""
        hashed = hash_password("")

        assert verify_password("", hashed) is True
        assert verify_password("not_empty", hashed) is False

    def test_verify_password_case_sensitive(self):
        """Test that password verification is case sensitive."""
        password = "CaseSensitive"
        hashed = hash_password(password)

        assert verify_password("CaseSensitive", hashed) is True
        assert verify_password("casesensitive", hashed) is False
        assert verify_password("CASESENSITIVE", hashed) is False

    def test_verify_password_special_characters(self):
        """Test verifying password with special characters."""
        password = "p@$$w0rd!#%"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True
        assert verify_password("p@$$w0rd!#", hashed) is False

    def test_verify_password_unicode(self):
        """Test verifying password with unicode characters."""
        password = "パスワード123"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True
        assert verify_password("パスワード", hashed) is False

    def test_verify_password_invalid_hash(self):
        """Test verifying with invalid hash string."""
        assert verify_password("password", "invalid_hash") is False
        assert verify_password("password", "") is False

    def test_verify_password_whitespace_matters(self):
        """Test that whitespace in password matters."""
        password = "password with spaces"
        hashed = hash_password(password)

        assert verify_password("password with spaces", hashed) is True
        assert verify_password("passwordwithspaces", hashed) is False
        assert verify_password(" password with spaces ", hashed) is False


class TestJWTTokenCreation:
    """Test cases for JWT token creation."""

    def test_create_access_token_basic(self):
        """Test creating a basic access token."""
        data = {"sub": "123", "email": "user@example.com"}
        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_payload(self):
        """Test that token contains correct payload data."""
        data = {"sub": "123", "email": "user@example.com", "user_type": "volunteer"}
        token = create_access_token(data)

        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

        assert payload["sub"] == "123"
        assert payload["email"] == "user@example.com"
        assert payload["user_type"] == "volunteer"
        assert "exp" in payload

    def test_create_access_token_expiration_default(self):
        """Test that token has default expiration time."""
        data = {"sub": "123"}
        token = create_access_token(data)

        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        exp_timestamp = payload["exp"]

        # Check that expiration is set
        assert exp_timestamp is not None
        assert isinstance(exp_timestamp, int)

    def test_create_access_token_custom_expiration(self):
        """Test creating token with custom expiration."""
        data = {"sub": "123"}
        expires_delta = timedelta(minutes=5)
        token = create_access_token(data, expires_delta=expires_delta)

        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        exp_timestamp = payload["exp"]
        exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        now = datetime.now(timezone.utc)

        # Should expire in approximately 5 minutes
        time_diff = exp_datetime - now
        assert 4 * 60 < time_diff.total_seconds() < 6 * 60

    def test_create_access_token_empty_data(self):
        """Test creating token with minimal data."""
        data = {}
        token = create_access_token(data)

        assert isinstance(token, str)
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        assert "exp" in payload

    def test_create_access_token_various_data_types(self):
        """Test creating token with various data types."""
        data = {"sub": "123", "number": 42, "boolean": True, "list": [1, 2, 3], "nested": {"key": "value"}}
        token = create_access_token(data)

        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        assert payload["sub"] == "123"
        assert payload["number"] == 42
        assert payload["boolean"] is True
        assert payload["list"] == [1, 2, 3]
        assert payload["nested"] == {"key": "value"}


class TestJWTTokenDecoding:
    """Test cases for JWT token decoding."""

    def test_decode_access_token_valid(self):
        """Test decoding a valid token."""
        data = {"sub": "123", "email": "user@example.com"}
        token = create_access_token(data)

        payload = decode_access_token(token)

        assert payload["sub"] == "123"
        assert payload["email"] == "user@example.com"
        assert "exp" in payload

    def test_decode_access_token_expired(self):
        """Test decoding an expired token."""
        data = {"sub": "123"}
        # Create token that expires immediately
        expires_delta = timedelta(seconds=-1)
        token = create_access_token(data, expires_delta=expires_delta)

        with pytest.raises(HTTPException) as exc_info:
            decode_access_token(token)

        assert exc_info.value.status_code == 401
        assert "expired" in exc_info.value.detail.lower()

    def test_decode_access_token_invalid(self):
        """Test decoding an invalid token."""
        invalid_token = "this.is.invalid"

        with pytest.raises(HTTPException) as exc_info:
            decode_access_token(invalid_token)

        assert exc_info.value.status_code == 401
        assert "invalid" in exc_info.value.detail.lower()

    def test_decode_access_token_malformed(self):
        """Test decoding a malformed token."""
        malformed_tokens = [
            "",
            "not_a_token",
            "header.payload",
            "too.many.parts.here",
        ]

        for token in malformed_tokens:
            with pytest.raises(HTTPException) as exc_info:
                decode_access_token(token)
            assert exc_info.value.status_code == 401

    def test_decode_access_token_wrong_secret(self):
        """Test that token signed with different secret is invalid."""
        data = {"sub": "123"}
        # Create token with different secret
        wrong_token = jwt.encode(data, "wrong_secret", algorithm=JWT_ALGORITHM)

        with pytest.raises(HTTPException) as exc_info:
            decode_access_token(wrong_token)

        assert exc_info.value.status_code == 401

    def test_decode_access_token_wrong_algorithm(self):
        """Test that token with different algorithm is invalid."""
        data = {"sub": "123"}
        # Create token with different algorithm
        wrong_token = jwt.encode(data, JWT_SECRET_KEY, algorithm="HS512")

        with pytest.raises(HTTPException) as exc_info:
            decode_access_token(wrong_token)

        assert exc_info.value.status_code == 401

    def test_decode_access_token_preserves_data(self):
        """Test that decoding preserves all original data."""
        original_data = {
            "sub": "456",
            "email": "test@example.com",
            "user_type": "organisation",
            "custom_field": "custom_value",
        }
        token = create_access_token(original_data)

        decoded = decode_access_token(token)

        for key, value in original_data.items():
            assert decoded[key] == value


class TestPasswordHashingIntegration:
    """Integration tests for password hashing workflow."""

    def test_full_password_workflow(self):
        """Test complete password hash and verify workflow."""
        original_password = "MySecurePassword123!"

        # Hash the password
        hashed = hash_password(original_password)

        # Verify correct password
        assert verify_password(original_password, hashed) is True

        # Verify incorrect password
        assert verify_password("WrongPassword", hashed) is False

    def test_multiple_users_same_password(self):
        """Test that multiple users can have the same password with different hashes."""
        password = "common_password"

        hash1 = hash_password(password)
        hash2 = hash_password(password)
        hash3 = hash_password(password)

        # All hashes should be different
        assert hash1 != hash2
        assert hash2 != hash3
        assert hash1 != hash3

        # But all should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True
        assert verify_password(password, hash3) is True


class TestJWTTokenIntegration:
    """Integration tests for JWT token workflow."""

    def test_full_token_workflow(self):
        """Test complete token creation and decoding workflow."""
        user_data = {"sub": "789", "email": "integration@example.com", "user_type": "coordinator"}

        # Create token
        token = create_access_token(user_data)

        # Decode token
        decoded = decode_access_token(token)

        # Verify data
        assert decoded["sub"] == user_data["sub"]
        assert decoded["email"] == user_data["email"]
        assert decoded["user_type"] == user_data["user_type"]

    def test_token_lifecycle(self):
        """Test token creation with short expiration and lifecycle."""
        data = {"sub": "123"}

        # Create token with 2 second expiration
        expires_delta = timedelta(seconds=2)
        token = create_access_token(data, expires_delta=expires_delta)

        # Should be valid immediately
        payload = decode_access_token(token)
        assert payload["sub"] == "123"

        # Import time for sleep
        import time

        # Wait for expiration
        time.sleep(3)

        # Should now be expired
        with pytest.raises(HTTPException) as exc_info:
            decode_access_token(token)

        assert exc_info.value.status_code == 401
        assert "expired" in exc_info.value.detail.lower()
