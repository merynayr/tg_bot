import os
import zipfile

PROJECT_DIR = './'  # корень проекта
ARCHIVE_NAME = 'project_archive.zip'
SCRIPT_NAME = os.path.basename(__file__)  # имя текущего скрипта

EXCLUDE_DIRS = {'venv', 'env', '__pycache__', '.git', '.idea', '.pytest_cache'}
EXCLUDE_EXTS = {'.log', '.pyc', '.pyo', '.tmp', '.swp', '.DS_Store', '.pkl'}

def should_exclude(file_path):
    parts = file_path.split(os.sep)
    if any(p in EXCLUDE_DIRS for p in parts):
        return True
    _, ext = os.path.splitext(file_path)
    if ext.lower() in EXCLUDE_EXTS:
        return True
    # исключаем сам скрипт
    if os.path.basename(file_path) == SCRIPT_NAME:
        return True
    return False

def create_archive():
    with zipfile.ZipFile(ARCHIVE_NAME, 'w', zipfile.ZIP_DEFLATED) as archive:
        for root, dirs, files in os.walk(PROJECT_DIR):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                file_path = os.path.join(root, file)
                if should_exclude(file_path):
                    continue
                rel_path = os.path.relpath(file_path, PROJECT_DIR)
                archive.write(file_path, rel_path)
                print(f'Добавлен: {rel_path}')

    print(f'Архивация завершена, файл: {ARCHIVE_NAME}')

if __name__ == '__main__':
    create_archive()
