import unittest
from unittest.mock import patch, MagicMock
import json
from config2 import generate_graphviz, get_npm_dependencies, get_transitive_dependencies


class TestDependencyGraph(unittest.TestCase):

    def test_generate_graphviz(self):
        # Тест на корректность генерации графа
        graph = {
            "package1": {"dep1": {}, "dep2": {}},
            "package2": {"dep3": {}},
        }
        expected_output = (
            'digraph G {\n'
            '"package1" -> "dep1";\n'
            '"package1" -> "dep2";\n'
            '"package2" -> "dep3";\n'
            '}\n'
        )
        self.assertEqual(generate_graphviz(graph), expected_output)

    @patch('config2.requests.get')
    def test_get_npm_dependencies(self, mock_get):
        # Создание фейкового ответа от API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'dist-tags': {'latest': '1.0.0'},
            'versions': {
                '1.0.0': {'dependencies': {'dep1': '^1.0.0', 'dep2': '^2.0.0'}}
            },
        }
        mock_get.return_value = mock_response

        result = get_npm_dependencies('test-package', 'https://fake-repo.com/')
        expected_result = {'dep1': '^1.0.0', 'dep2': '^2.0.0'}

        self.assertEqual(result, expected_result)
        mock_get.assert_called_with('https://fake-repo.com/test-package')


if __name__ == '__main__':
    unittest.main()
