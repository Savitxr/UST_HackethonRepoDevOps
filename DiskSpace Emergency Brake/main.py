
import os
import zipfile
import platform
import time

def get_disk_usage(partition):
    if platform.system() == "Windows":
        import shutil
        total, used, free = shutil.disk_usage(partition)
        return used / total * 100
    else:
        st = os.statvfs(partition)
        total = st.f_blocks * st.f_frsize
        free = st.f_bfree * st.f_frsize
        used = total - free
        return used / total * 100

def get_largest_files(partition, n=5):
    largest_files = []
    for root, dirs, files in os.walk(partition):
        for file in files:
            try:
                path = os.path.join(root, file)
                size = os.path.getsize(path)
                largest_files.append((size, path))
            except Exception as e:
                print(f"Error accessing {path}: {e}")
    largest_files.sort(reverse=True)
    return largest_files[:n]

def compress_files(files, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for size, file in files:
            zipf.write(file, os.path.basename(file))
            print(f"Compressed {file} ({size} bytes)")

def main():
    partition = "C:\\" if platform.system() == "Windows" else "/"
    while True:
        usage = get_disk_usage(partition)
        print(f"Disk usage: {usage:.2f}%")
        if usage >= 40:
            print("Disk usage critical! Identifying largest files...")
            largest_files = get_largest_files(partition)
            output_zip = os.path.join("/tmp", "largest_files.zip") if platform.system() != "Windows" else os.path.join(os.getenv("TEMP"), "largest_files.zip")
            compress_files(largest_files, output_zip)
            print(f"Moved largest files to {output_zip}")
        time.sleep(5)  

if __name__ == "__main__":
    main()
