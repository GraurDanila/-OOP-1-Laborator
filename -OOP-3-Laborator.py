import os
import time
import datetime

class File:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.extension = os.path.splitext(self.name)[1]

    def get_info(self):
        return f"Name: {self.name}, Extension: {self.extension}"


class TextFile(File):
    def __init__(self, path):
        super().__init__(path)

    def get_info(self):
        info = super().get_info()
        with open(self.path, 'r') as file:
            content = file.read()
            line_count = content.count('\n') + 1
            word_count = len(content.split())
            char_count = len(content)
        return f"{info}, Line count: {line_count}, Word count: {word_count}, Character count: {char_count}"


class ImageFile(File):
    def __init__(self, path):
        super().__init__(path)

    def get_info(self):
        info = super().get_info()
        size = "Unknown"
        if self.extension.lower() in ['.png', '.jpg']:
            try:
                width, height = self._get_image_size()
                size = f"{width}x{height}"
            except Exception as e:
                print(f"Error getting image size: {e}")
        return f"{info}, Image size: {size}"

    def _get_image_size(self):
        return 1024, 768  


class ProgramFile(File):
    def __init__(self, path):
        super().__init__(path)

    def get_info(self):
        info = super().get_info()
        line_count = 0
        class_count = 0
        method_count = 0
        return f"{info}, Line count: {line_count}, Class count: {class_count}, Method count: {method_count}"


class FolderMonitor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        if not os.path.isdir(folder_path):
            raise ValueError(f"Folder '{folder_path}' does not exist.")
        self.files = self._load_files()
        self.snapshot_time = self.load_snapshot_time()  # încarcă snapshot-ul anterior sau None dacă nu există

    def _load_files(self):
        files = []
        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(file_path):
                if filename.endswith('.txt'):
                    files.append(TextFile(file_path))
                elif filename.endswith(('.png', '.jpg')):
                    files.append(ImageFile(file_path))
                elif filename.endswith(('.py', '.java')):
                    files.append(ProgramFile(file_path))
        return files

    # salvarea snapshot-ului în fișier text
    def commit(self):
        self.snapshot_time = datetime.datetime.now()
        self.save_snapshot_time()  

    def save_snapshot_time(self):
        snapshot_file_path = os.path.join(self.folder_path, 'snapshot.txt')
        with open(snapshot_file_path, 'w') as snapshot_file:
            snapshot_file.write(str(self.snapshot_time))

    def load_snapshot_time(self):
        snapshot_file_path = os.path.join(self.folder_path, 'snapshot.txt')
        if os.path.isfile(snapshot_file_path):
            with open(snapshot_file_path, 'r') as snapshot_file:
                snapshot_time_str = snapshot_file.read()
                return datetime.datetime.strptime(snapshot_time_str, '%Y-%m-%d %H:%M:%S.%f')
        return None

    def info(self, filename):
        for file in self.files:
            if file.name == filename:
                print(file.get_info())
                return
        print("File not found.")

    def status(self):
        if self.snapshot_time is None:
            print("No snapshot taken yet.")
            return
        print("Status:")
        for file in self.files:
            print(file.name)
           
            # Checkiuieste daca failul a fost modificat dupa snapshot
            modified_time = os.path.getmtime(file.path)
            modified_datetime = datetime.datetime.fromtimestamp(modified_time)
            if modified_datetime > self.snapshot_time:
                print(" - Modified")
            else:
                print(" - Not modified")

    def monitor_changes(self):
    while True:
        time.sleep(5)  # Checkuieste la fiecare 5 secunde
        if self.snapshot_time is None:
            continue  # Nu face nimic dacă nu avem un snapshot
        for file in self.files:
            modified_time = os.path.getmtime(file.path)
            modified_datetime = datetime.datetime.fromtimestamp(modified_time)
            if modified_datetime > self.snapshot_time:
                print(f"Change detected in file: {file.name}")

if __name__ == "__main__":
    folder_path = r"C:\Users\Danila\Desktop\OOP3"
    monitor = FolderMonitor(folder_path)

    # monitorizeaza modificarile
    import threading
    monitor_thread = threading.Thread(target=monitor.monitor_changes)
    monitor_thread.daemon = True
    monitor_thread.start()

    while True:
        command = input("Enter command (commit/info <filename>/status): ").split()
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
            print("Invalid command.")