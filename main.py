# This is a sample Python script.
import multiprocessing
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import re

import tensorflow as tf
import hashlib
import urllib3


global_files = 0
global_array = []
global_samefile = []
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def get_file(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files

def get_file_number(i, folder_array):
    global global_files
    global global_array

    for item in folder_array:
        global_array.append(item)
    global_files = global_files + i
    print("The global files no: ", global_files)

def get_folder(folder_path):

    for root, dirs, files in os.walk(folder_path):
        for folder in dirs:
            folder_name = os.path.join(root, folder)
            print(f"Folder: {folder_name} \n")
            all_file_in_folder = get_file(folder_name)
            get_file_number(len(all_file_in_folder), all_file_in_folder)
            if all_file_in_folder:
                print(f"All files in {folder_name}:\n")
                for file_path in all_file_in_folder:
                    print(file_path)
            else:
                print(f"No files found in {folder_name}")
        for file_name in files:
            subfolder_path = os.path.join(root, file_name)
            get_folder(subfolder_path)

def compare_files_hash(file1_path, file2_path, hash_function=hashlib.sha256):
    # print(f"first file {file1_path}\nsecond file {file2_path}")
    with open(file1_path, 'rb') as file1:
        hash1 = hash_function(file1.read()).hexdigest()
    with open(file2_path, 'rb') as file2:
        hash2 = hash_function(file2.read()).hexdigest()

    if hash1 == hash2:
        print(f"File are identical {file1_path}. with {file2_path}\n")

def max_compare_files_hash(args):
    file1_path, file2_path, hash_function = args
    # print(f"First file {file1_path}\nSecond file {file2_path}")
    with open(file1_path, 'rb') as file1:
        hash1 = hash_function(file1.read()).hexdigest()

    with open(file2_path, 'rb') as file2:
        hash2 = hash_function(file2.read()).hexdigest()

    if hash1 == hash2:
        print(f"Files are identical: {file1_path} and {file2_path}")

def process_files(file_path, hash_function=hashlib.sha256):
    with multiprocessing.Pool() as pool:
        pool.map(max_compare_files_hash, [(file1, file2, hash_function) for file1, file2 in file_path])


# Press the green button in the gutter to run the script.
# urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)
gpus = tf.config.list_physical_devices('GPU')
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
print("TensorFlow version:", tf.__version__)
for gpu in gpus:
    print("Name: ", gpu.name, "Type: ", gpu.device_type)
if __name__ == '__main__':
    print_hi('PyCharm')
    num_tasks = 10
    get_folder("/Volumes/LaCie/Files from old Drives/Disk01/Musics")
    # get_folder("/Volumes/LaCie/Files from old Drives/Disk02")
    # get_folder("/Volumes/LaCie/Files from old Drives/Disk03")
    ds_store_patten = re.compile(r'/\.DS_Store$')
    plist_pattern = re.compile(r'\.plist$')
    tdb_pattern = re.compile(r'\.db$')
    ipa_pattern = re.compile(r'\.ipa$')
    print(global_array)
    i = 0
    file_pairs = [(file1, file2) for i, file1 in enumerate(global_array) for file2 in global_array[i + 1:]]
    process_files(file_pairs)
    # for file1_path in global_array:
    #     if ds_store_patten.search(file1_path) or plist_pattern.search(file1_path) or tdb_pattern.search(file1_path) or ipa_pattern.search(file1_path):
    #         continue
    #     j = 0
    #     for file2_path in global_array:
    #         if i == j:
    #             j += 1
    #             continue
    #         compare_files_hash(file1_path, file2_path)
    #         j += 1
    #     i += 1


# print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices("GPU")))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
