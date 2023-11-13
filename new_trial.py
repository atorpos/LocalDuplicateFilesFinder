import os
import hashlib
import concurrent.futures
import shutil


def calculate_hash(file_path, block_size=65536):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        for block in iter(lambda: file.read(block_size), b''):
            hasher.update(block)
    return hasher.hexdigest()


def process_files(file_paths):
    file_hashes = {}

    for file_path in file_paths:
        file_hash = calculate_hash(file_path)

        if file_hash in file_hashes:
            file_hashes[file_hash].append(file_path)
        else:
            file_hashes[file_hash] = [file_path]

    return file_hashes


def move_file(source_path, dest_path):
    # destination_path = "/Volumes/LaCie/D3_Duplicate"
    destination_path = dest_path
    try:
        source_filename = os.path.basename(source_path)
        destination_filename = os.path.join(destination_path, source_filename)
        shutil.move(source_path, destination_filename)
        print(f"File '{source_filename}' move successfully to '{destination_path}'")
    except Exception as e:
        print(f"Error moving file: {e}")
def find_duplicate_files(folder_path, dest_path):
    all_files = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            all_files.append(file_path)

    batch_size = 5000  # Adjust the batch size based on your system's capabilities
    with concurrent.futures.ThreadPoolExecutor() as executor:
        file_batches = [all_files[i:i + batch_size] for i in range(0, len(all_files), batch_size)]
        results = list(executor.map(process_files, file_batches))

    # Merge results
    final_hashes = {}
    for result in results:
        for hash_value, files in result.items():
            if hash_value in final_hashes:
                final_hashes[hash_value].extend(files)
            else:
                final_hashes[hash_value] = files

    # Filter out non-duplicates
    duplicate_files = {hash_value: files for hash_value, files in final_hashes.items() if len(files) > 1}

    print("Duplicate files found:")
    for hash_value, files in duplicate_files.items():
        i = 0;
        for file_path in files:
            if i == 0:
                i +=1
                continue
            print("File:", file_path)
            move_file(file_path, dest_path)
        print("---")


# Example usage
if __name__ == '__main__':
    user_folder_path = input("Input the folder you would like the run")
    moving_folder_path = input("Input the duplicated files you would like to store")
    # folder_path = user_foler_path
    find_duplicate_files(user_folder_path, moving_folder_path)