import pytest
import os
from typing import List
from src.utils.files import (
    create_file,
    read_file,
    write_to_file,
    append_to_file
)


class TestCreateFile:   
    @pytest.mark.parametrize('file_path_suffix,should_create_dir', [
        ('test.txt', False),
        ('subdir/test.txt', True),
        ('level1/level2/level3/test.txt', True),
    ], ids=['existing_dir', 'new_dir', 'nested_dirs'])
    def test_create_file(self, temp_dir: str, file_path_suffix: str, should_create_dir: bool) -> None:
        file_path: str = os.path.join(temp_dir, file_path_suffix)
        create_file(file_path)
        assert os.path.exists(file_path)
        assert os.path.isfile(file_path)
        if should_create_dir:
            assert os.path.exists(os.path.dirname(file_path))


class TestReadFile:   
    @pytest.mark.parametrize('content, file_exists', [
        ('Hello, World!', True),
        ('', True),
        ('Line 1\nLine 2\nLine 3', True),
        ('', False),
    ], ids=['happy_simple_text', 'happy_empty_file', 'happy_multiline', 'sad_nonexistent'])
    def test_read_file(self, temp_dir: str, content: str, file_exists: bool) -> None:
        file_path: str = os.path.join(temp_dir, 'test.txt')
        if file_exists:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            result: str | None = read_file(file_path)
            assert result == content
        else:
            result: str | None = read_file(file_path)
            assert result is None


class TestWriteToFile:   
    @pytest.mark.parametrize('content, file_path_suffix, expected_result', [
        ('Test content', 'test.txt', True),
        ('', 'test.txt', True),
        ('A' * 10000, 'test.txt', True),
        ('!@#$%^&*()_+-=[]{}|;:,.<>?', 'test.txt', True),
        ('Test content', 'subdir/test.txt', True),
    ], ids=['simple', 'empty', 'large', 'special_chars', 'creates_dir'])
    def test_write_to_file(self, temp_dir: str, content: str, file_path_suffix: str, expected_result: bool) -> None:
        file_path: str = os.path.join(temp_dir, file_path_suffix)
        result: bool = write_to_file(file_path, content)
        assert result == expected_result
        assert os.path.exists(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            assert f.read() == content


class TestAppendToFile:   
    @pytest.mark.parametrize('lines, file_path_suffix, expected_result', [
        (['First line'], 'test.txt', True),
        (['First line', 'Second line'], 'test.txt', True),
        (['Line 1', 'Line 2', 'Line 3'], 'test.txt', True),
        ([''], 'test.txt', True),
        (['Hello, 世界! 🌍'], 'test.txt', True),
        (['First line'], 'subdir/test.txt', True),
    ], ids=['single_line', 'two_lines', 'multiple_lines', 'empty_line', 'unicode', 'creates_dir'])
    def test_append_to_file(self, temp_dir: str, lines: List[str], file_path_suffix: str, expected_result: bool) -> None:
        file_path: str = os.path.join(temp_dir, file_path_suffix)
        for line in lines:
            result: bool = append_to_file(file_path, line)
            assert result == expected_result
        assert os.path.exists(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            read_lines: List[str] = f.readlines()
            assert len(read_lines) == len(lines)
            for i, line in enumerate(lines):
                assert read_lines[i] == line + '\n'
