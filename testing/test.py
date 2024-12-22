import os


for path, subdirs, files in os.walk(r"data\pdf"):
    for name in files:
        file = os.path.join(path, name)
        print(file)
