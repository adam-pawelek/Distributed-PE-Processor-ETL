import os
from pathlib import Path

THIS_DIR = Path(__file__).parent
# Define the folder path
folder_path = THIS_DIR.parent / 'data/binary_files_data/'


def get_binary_files():
    # Ensure the folder exists
    print(folder_path)

    if os.path.exists(folder_path):

        # List all files in the folder
        files = os.listdir(folder_path)

        # Define a dictionary to hold file contents
        file_contents = {}

        # Loop through each file
        for file_name in files:
            # Build full path
            file_path = os.path.join(folder_path, file_name)

            # Ensure it's a file
            if os.path.isfile(file_path):
                # Open the file in binary mode and read the contents
                with open(file_path, 'rb') as file:
                    file_contents[file_name] = file.read()

        return file_contents

    else:
        print("Folder does not exist!")


