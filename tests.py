import unittest
from unittest.mock import patch, MagicMock
import json
from io import StringIO

# Импортируем функции для тестирования
from config2 import build_graphviz_code, resolve_dependencies, write_to_file


class TestDependencyVisualizer(unittest.TestCase):
    def test_build_graphviz_code(self):
        """Тест генерации кода Graphviz"""
        deps = {
            "packageA": {"packageB", "packageC"},
            "packageB": {"packageD"},
            "packageC": {},
            "packageD": {},
        }
        expected_output = (
            "digraph Dependencies {\n"
            '  "packageA" -> "packageB"\n'
            '  "packageA" -> "packageC"\n'
            '  "packageB" -> "packageD"\n'
            "}\n"
        )
        self.assertEqual(build_graphviz_code(deps), expected_output)

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_write_to_file(self, mock_open):
        """Тест записи в файл"""
        test_content = "Test content"
        write_to_file("test.dot", test_content)
        mock_open.assert_called_once_with("test.dot", "w")
        mock_open().write.assert_called_once_with(test_content)
