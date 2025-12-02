import pytest
from bson import ObjectId
from src.utils.db import str_to_object_id


class TestStrToObjectId:
    @pytest.mark.parametrize('id_str, expected_valid', [
        ('507f1f77bcf86cd799439011', True),
        ('000000000000000000000000', True),
        ('507F1F77BCF86CD799439011', True),
    ], ids=['valid', 'valid_all_zeros', 'valid_uppercase'])
    def test_happy_str_to_object_id(self, id_str: str, expected_valid: bool) -> None:
        result: ObjectId = str_to_object_id(id_str)
        assert isinstance(result, ObjectId) == expected_valid

    @pytest.mark.parametrize('id_str', [
        '123',
        'not-a-valid-object-id',
        '',
        '507f1f77bcf86cd79943901!',
        '507f1f77bcf86cd7994390111',
        '507f1f77bcf86cd79943901g',
    ], ids=['invalid_short', 'invalid_format', 'invalid_empty', 'invalid_special', 'invalid_too_long', 'invalid_non_hex'])
    def test_sad_str_to_object_id(self, id_str: str) -> None:
        with pytest.raises(ValueError, match='Invalid ObjectId'):
            str_to_object_id(id_str)
