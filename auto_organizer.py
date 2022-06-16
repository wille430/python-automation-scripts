from watchdog.observers import Observer
import os
import time
import shutil


class Organizer():

    def __init__(self, downloads_dir=os.path.join(os.path.expanduser('~'), "Downloads"), archive_dir=os.path.join(os.path.expanduser('~'), "Downloads/archive"), delete_older_than=(time.time() - 14 * 24 * 60 * 60)) -> None:
        self.downloads_dir = downloads_dir
        self.archive_dir = archive_dir

        self.delete_older_than = delete_older_than

        self.formats = {
            'audio': ['mp3', 'wav'],
            'video': ['mp4', 'mov'],
            'image': ['png', 'jpg', 'jpeg', 'gif'],
        }
        self.dest_dirs = {
            'image': os.path.join(downloads_dir, 'images'),
            'video': os.path.join(downloads_dir, 'videos'),
            'audio': os.path.join(downloads_dir, 'audio')
        }

        for key in self.dest_dirs.keys():
            if (not os.path.exists(self.dest_dirs[key])):
                os.mkdir(self.dest_dirs[key])

    def organize(self):
        for filename in os.listdir(self.downloads_dir):
            file_path = os.path.join(self.downloads_dir, filename)
            file_extensions = filename.split('.')[-1]

            if not os.path.isfile(file_path):
                continue

            for format in self.dest_dirs.keys():
                if file_extensions in self.formats[format]:
                    print(
                        f"Moving {format} {filename} to {self.dest_dirs[format]}")
                    shutil.move(file_path, os.path.join(
                        self.dest_dirs[format], filename))
                    break

    def archive_old(self):
        for filename in os.listdir(self.downloads_dir):
            file_path = os.path.join(self.downloads_dir, filename)

            if file_path == self.archive_dir:
                continue

            created_time = os.path.getmtime(file_path)

            if created_time < self.delete_older_than:
                to_src = os.path.join(self.archive_dir, filename)
                shutil.move(file_path, to_src)


def main():

    organizer = Organizer()

    organizer.archive_old()

    observer = Observer()
    observer.schedule(organizer.organize(), organizer.downloads_dir)

    print(f"Observing file changes in {organizer.downloads_dir}...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    main()
