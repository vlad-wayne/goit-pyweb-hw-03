import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def copy_file(file_path, target_root):
    file_extension = os.path.splitext(file_path)[-1].lower().strip('.')
    if not file_extension:
        return

    target_dir = os.path.join(target_root, file_extension)
    create_directory(target_dir)

    target_path = os.path.join(target_dir, os.path.basename(file_path))
    shutil.copy2(file_path, target_path)

def process_directory(source_dir, target_dir, pool):
    try:
        with os.scandir(source_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    pool.submit(copy_file, entry.path, target_dir)
                elif entry.is_dir():
                    process_directory(entry.path, target_dir, pool)
    except PermissionError:
        print(f"Не вдалося отримати доступ до {source_dir}", file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        print("Використання: python sort_files.py <джерельна_директорія> [цільова_директорія]", file=sys.stderr)
        sys.exit(1)

    source_dir = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else 'dist'

    if not os.path.exists(source_dir):
        print(f"Джерельна директорія {source_dir} не існує.", file=sys.stderr)
        sys.exit(1)

    create_directory(target_dir)

    with ThreadPoolExecutor() as pool:
        process_directory(source_dir, target_dir, pool)

    print(f"Файли успішно відсортовано у директорії {target_dir}.")

if __name__ == "__main__":
    main()