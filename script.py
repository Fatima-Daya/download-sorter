#!/usr/bin/env python3

import argparse
import os
import time
import shutil
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileSorter(FileSystemEventHandler):
    def __init__(self, target_dir):
        super().__init__()
        self.target_dir = target_dir

    def on_created(self, event):
        if not event.is_directory:
            filename = event.src_path
            extension = os.path.splitext(filename)[1].lower()
            destination = self.get_destination(extension)
            self.move_file(filename, destination)

    def get_destination(self, extension):
        default_dir = os.path.join(self.target_dir, "Downloads")

        # Define mapping of file extensions to target directories
        extensions_mapping = {
            ".txt": "Documents",
            ".jpg": "Pictures",
            ".mp3": "Music",
            ".mp4": "Videos",
        }

        # Check if extension is mapped, otherwise use the default directory
        if extension in extensions_mapping:
            return os.path.join(self.target_dir, extensions_mapping[extension])
        else:
            return default_dir

    def move_file(self, source, destination):
        if not os.path.exists(destination):
            os.makedirs(destination)

        filename = os.path.basename(source)
        destination_file = os.path.join(destination, filename)

        # Move the file to the destination directory
        shutil.move(source, destination_file)
        print(f"Moved {filename} to {destination}")


def main(args):
    target_dir = args.directory

    # Create the observer and event handler
    observer = Observer()
    event_handler = FileSorter(target_dir)

    # Set up the observer to watch the target directory for file creations
    observer.schedule(event_handler, target_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Background file sorter script.")
    parser.add_argument("directory", type=str, help="Target directory to watch for file creations.")

    args = parser.parse_args()
    main(args)
