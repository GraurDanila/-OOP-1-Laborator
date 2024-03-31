import os
import datetime
import mimetypes
from abc import ABC, abstractmethod
from collections import defaultdict
import re
import threading
import time

class FileInfo(ABC):
    def __init__(self, filename):
        self.filename = filename

    @abstractmethod
    def get_info(self):
        pass

class ImageFileInfo(FileInfo):
    def get_info(self):
        file_path = os.path.join(folder_path, self.filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                image_data = f.read()
            return len(image_data)
        else:
            return None

class TextFileInfo(FileInfo):
    def get_info(self):
        file_path = os.path.join(folder_path, self.filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            line_count = len(lines)
            word_count = sum(len(line.split()) for line in lines)
            character_count = sum(len(line) for line in lines)
            return line_count, word_count, character_count
        else:
            return None

class ProgramFileInfo(FileInfo):
    def init(self, path):
        super().init(path)

    def get_info(self):
        info = super().get_info()
        line_count = 0
        class_count = 0
        method_count = 0
        words = []
        info = super().get_info()
        with open(self.path, 're') as file:
            content = file.read()
            lines = re.split("\n", content)
            words = re.split(" |\n", content)
            print(words)
            for word in words:
                match word:
                    case "def":
                        method_count = method_count + 1
                    case "class":
                        class_count = class_count + 1

        print(len(lines))
        print(class_count)
        print(method_count)
        return f"{info}, Line count: {line_count}, Class count: {class_count}, Method count: {method_count}"

class FileMonitor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.snapshot_time = None
        self.file_info = defaultdict(dict)
        self.instance = FileInfo
        self.file_type = None
        self.lock = threading.Lock()
        self.commit_time = None

    def get_file_instance(self, filename):
        file_path = os.path.join(self.folder_path, filename)
        if os.path.exists(file_path):
            file_type = mimetypes.guess_type(file_path)[0]
            self.file_type = file_type
            if file_type in ('image/png', 'image/jpeg'):
                instance = ImageFileInfo
            elif file_type == 'text/plain':
                instance = TextFileInfo
            elif file_type == 'text/x-python' or file_type == 'application/x-python-code':
                instance = ProgramFileInfo
            elif file_type == 'text/x-java-source':
                instance = ProgramFileInfo
            else:
                instance = FileInfo
            return instance
        else:
            return None

    def monitor_folder(self):
        with self.lock:
            current_files = set(os.listdir(self.folder_path))

            new_files = current_files - set(self.file_info.keys())
            for new_file in new_files:
                Instance = self.get_file_instance(new_file)
                if Instance:
                    self.file_info[new_file] = Instance(new_file).get_info()
                    print(f"{new_file} - File nou nouț") 

            for filename in current_files:
                if os.path.isfile(os.path.join(self.folder_path, filename)):
                    Instance = self.get_file_instance(filename)
                    if Instance:
                        self.file_info[filename] = Instance(filename).get_info()

    def info(self, filename):
        with self.lock:
            Instance = self.get_file_instance(filename)
            if Instance:
                file_instance = Instance(filename)
                file_info = file_instance.get_info()
                if file_info:
                    log_message = f"{datetime.datetime.now()} - Info requested for {filename}\n"
                    self.log_operation(log_message)
                    print(f"Name: {filename}")
                    print(f"Type: {self.file_type or file_instance.__class__.__name__}")
                    creation_time = os.path.getctime(os.path.join(self.folder_path, filename))
                    modification_time = os.path.getmtime(os.path.join(self.folder_path, filename))
                    print(f"Created: {datetime.datetime.fromtimestamp(creation_time)}")
                    print(f"Updated: {datetime.datetime.fromtimestamp(modification_time)}")

                    if isinstance(file_instance, ImageFileInfo):
                        print(f"Image Size: {file_info} bytes")
                    elif isinstance(file_instance, TextFileInfo):
                        print(f"Line Count: {file_info[0]}")
                        print(f"Word Count: {file_info[1]}")
                        print(f"Character Count: {file_info[2]}")
                    elif isinstance(file_instance, ProgramFileInfo) or isinstance(file_instance, ProgramFileInfo):
                        print(f"Line Count: {file_info[0]}")
                        print(f"Class Count: {file_info[1]}")
                        print(f"Method Count: {file_info[2]}")
                else:
                    print("File not found or does not exist.")

    def status(self):
        with self.lock:
            print("Status:")
            if not self.snapshot_time:
                print("No snapshot taken.")
                return

            current_files = set(os.listdir(self.folder_path))

            new_files = current_files - set(self.file_info.keys())
            for new_file in new_files:
                print(f"{new_file} - File nou nouț")

            deleted_files = set(self.file_info.keys()) - current_files
            for deleted_file in deleted_files:
                print(f"{deleted_file} - ȘTERS")

            print(f"Snapshot Time: {self.snapshot_time}")
            for filename, info in self.file_info.items():
                Instance = self.get_file_instance(filename)
                if Instance:
                    current_info = Instance(filename).get_info()
                    if current_info:
                        if current_info != info:
                            print(f"{filename} - So schimbat")
                        else:
                            print(f"{filename} - Nu so schimbat")
                    else:
                        print(f"{filename} - NU so gasit asa ceva")

    def commit(self):
      with self.lock:
        self.snapshot_time = datetime.datetime.now()
        self.commit_time = self.snapshot_time.strftime("%Y-%m-%d_%H-%M-%S") 
        
        file_stats = "\nFile Statistics:\n"
        for filename, info in self.file_info.items():
            file_stats += f"{filename} - {info}\n"

        log_message = f"{self.commit_time} - Manual commit performed\n{file_stats}\n"
        print("Snapshot taken.")
        
        commit_filename = os.path.join(folder_path, f"commit_{self.commit_time}.txt")
        with open(commit_filename, "w") as commit_file:
            commit_file.write(log_message)


def monitor_changes(monitor):
    while True:
        time.sleep(5)  # Checkuieste la fiecare 5 secunde
        if monitor.snapshot_time is None:
            continue  # Nu face nimic dacă nu avem un snapshot
        for file in monitor.files:
            modified_time = os.path.getmtime(file.path)
            modified_datetime = datetime.datetime.fromtimestamp(modified_time)
            if modified_datetime > monitor.snapshot_time:
                print(f"Transgender in failul: {file.name}")

if __name__ == "__main__":
    folder_path = r"C:\Users\Danila\Desktop\OOP3"   
    monitor = FileMonitor(folder_path)

    # monitorizeaza modificarile
    monitor_thread = threading.Thread(target=monitor.monitor_changes)
    monitor_thread.daemon = True
    monitor_thread.start()

    while True:
        command = input("Bagă șeva (commit/info <filename>/status): ").split()
        if command[0] == "commit":
            monitor.commit()
            print("Snapshot taken.")
        elif command[0] == "info":
            if len(command) == 2:
                monitor.info(command[1])
            else:
                print("Invalid command. Usage: info <filename>")
        elif command[0] == "status":
            monitor.status()
        else:
            print("Comanda invalida ca ROBU")
