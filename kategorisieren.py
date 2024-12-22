import os
import shutil

file_folder_path = r'C:\Users\silva\Desktop\testfolder'

for filename in os.listdir(file_folder_path):
    if not os.path.isdir(os.path.join(file_folder_path, filename)) and filename.endswith('.pdf'):
        first_part, second_part = filename.split('#')
        
        new_folder = os.path.join(file_folder_path, first_part)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

        old_file_path = os.path.join(file_folder_path, filename)
        new_file_name = second_part
        new_file_path = os.path.join(new_folder, new_file_name)
        
        shutil.move(old_file_path, new_file_path)