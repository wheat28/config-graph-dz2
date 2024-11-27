import os
import urllib.request
import json

def build_graphviz_code(dict_of_deps):
    code_from_graph = "digraph Dependencies {\n"
    for package, depends in dict_of_deps.items():
        for dep in depends:
            code_from_graph += f'  "{package}" -> "{dep}"\n'
    code_from_graph += "}\n"
    return code_from_graph

def get_npm_dependencies(pkg_name, repository_url):
    npm_url = f'{repository_url}/{pkg_name}'  # Используем URL из конфигурации

    try:
        with urllib.request.urlopen(npm_url) as response:
            if response.status != 200:
                raise Exception(f"Ошибка получения данных пакета: {response.status}")
            package_info = json.loads(response.read().decode())

    except urllib.error.URLError as e:
        raise Exception(f"Ошибка сети или неверный URL: {e}")
    except json.JSONDecodeError:
        raise Exception("Ошибка разбора JSON ответа.")

    latest_version = package_info['dist-tags']['latest']
    return package_info['versions'][latest_version].get('dependencies', {})

def resolve_dependencies(pkg_name, dict_of_deps, registry_url):
    if pkg_name in dict_of_deps:
        return dict_of_deps

    try:
        dependencies = get_npm_dependencies(pkg_name, registry_url)
        dict_of_deps[pkg_name] = dependencies
        for dep in dependencies:
            resolve_dependencies(dep, dict_of_deps, registry_url)

    except Exception as e:
        print(f"Ошибка обработки пакета {pkg_name}: {e}")

    return dict_of_deps

def write_to_file(file_path, code_of_deps):
    try:
        with open(file_path, 'w') as file:
            file.write(code_of_deps)
        print(f"Данные успешно сохранены в {file_path}")
    except IOError as err:
        print(f"Ошибка записи файла: {err}")

def run():
    configuration_filename = 'config.json'  # Используем JSON-файл
    try:
        with open(configuration_filename, 'r') as config_file:
            settings = json.load(config_file)

    except json.JSONDecodeError as err:
        print(f"Ошибка разбора конфигурационного файла: {err}")
        return

    graphviz_path = settings.get('graphviz_path')
    package_name = settings.get('package_name')
    output_file = settings.get('path_to_result_file')
    repository_url = settings.get('repository_url')

    if not package_name:
        print("Имя пакета не указано в конфигурации.")
        return

    print(f"Происходит получение зависимостей пакета {package_name}")
    dependencies = resolve_dependencies(package_name, {}, repository_url)

    graphviz_output = build_graphviz_code(dependencies)

    print("Сгенерированный Graphviz код:")
    print(graphviz_output)

    write_to_file(output_file, graphviz_output)

if __name__ == '__main__':
    run()
