import pytest
from src.security.password import hash_password, verify_password


class TestHashPassword:
    @pytest.mark.parametrize('password, expected_result', [
        ('test_password_123', True),
        ('', True   ),
        ('!@#$%^&*()_+-=[]{}|;:,.<>?', True),
        ('пароль密码🔒', True),
        ('A' * 1000, True),
        ('   password with spaces   ', True),
    ], ids=['simple', 'empty', 'special_chars', 'unicode', 'long', 'whitespace'])
    def test_hash_password(self, password: str, expected_result: bool) -> None:
        result: str = hash_password(password)
        assert isinstance(result, str) == expected_result
        assert (len(result) > 0) == expected_result


class TestVerifyPassword:   
    @pytest.mark.parametrize('password, verify_password_input, use_invalid_hash, expected_result', [
        ('test_password_123', 'test_password_123', False, True),
        ('test_password_123', 'wrong_password', False, False),
        ('', '', False, True),
        ('', 'not_empty', False, False),
        ('!@#$%^&*()_+-=[]{}|;:,.<>?', '!@#$%^&*()_+-=[]{}|;:,.<>?', False, True),
        ('пароль密码🔒', 'пароль密码🔒', False, True),
        ('test_password', 'test_password', False, True),
        ('TestPassword123', 'testpassword123', False, False),
        ('TestPassword123', 'TESTPASSWORD123', False, False),
        ('password123', 'password', False, False),
        ('password123', ' password123 ', False, False),
        ('A' * 1000, 'A' * 1000, False, True),
        ('test_password', 'test_password', True, False),
    ], ids=['correct', 'incorrect', 'empty_correct', 'empty_incorrect', 'special_correct', 'unicode_correct', 'correct_verify', 'case_lower', 'case_upper', 'partial', 'whitespace', 'long', 'invalid_hash'])
    def test_verify_password(self, password: str, verify_password_input: str, use_invalid_hash: bool, expected_result: bool) -> None:
        if use_invalid_hash:
            invalid_hash: str = 'not_a_valid_bcrypt_hash'
            result: bool = verify_password(verify_password_input, invalid_hash)
        else:
            hashed: str = hash_password(password)
            result: bool = verify_password(verify_password_input, hashed)
        assert result == expected_result
