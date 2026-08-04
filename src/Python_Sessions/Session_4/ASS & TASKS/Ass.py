import os
import random


def thanous_project():
    """
    Create files inside a folder, then delete half of them randomly.

    :return: None
    :rtype: None
    """

    folder_name = "Thanous"
    os.makedirs(folder_name, exist_ok=True)
    num_files = int(input("Enter the number of files: "))

    for i in range(1, num_files + 1):
        file_name = os.path.join(folder_name, f"file{i}.txt")
        open(file_name, "w").close()
    files = os.listdir(folder_name)
    print(f"\nNumber of files before deleting: {len(files)}")
    num_to_delete = len(files) // 2
    random_files = random.sample(files, num_to_delete)

    for file in random_files:
        file_path = os.path.join(folder_name, file)
        os.remove(file_path)

    
    remaining_files = os.listdir(folder_name)

    print(f"Number of files after deleting: {len(remaining_files)}")
    print("\nRemaining Files:")
    for file in remaining_files:
        print(file)


def main():
    thanous_project()


main()