import argparse
import logging
import os
import shutil
import subprocess
from datetime import datetime

def setup_logging():
    """Configures logging to output to both stdout and a log file."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            # logging.FileHandler("backup_process.log", encoding="utf-8")
        ]
    )

def get_7z_executable():
    """Checks whether 7z or 7za is available on the system PATH."""
    if shutil.which("7z"):
        return "7z"
    elif shutil.which("7za"):
        return "7za"
    return "C:/Program Files/7-Zip/7z.exe"

def main():
    setup_logging()
    
    # 1. Verify 7-Zip CLI tool exists on system
    seven_zip_cmd = get_7z_executable()
    if not seven_zip_cmd:
        logging.error("Error: '7z' or '7za' executable not found on this system. Please install 7-Zip.")
        return

    # 2. Parse CLI arguments using argparse
    parser = argparse.ArgumentParser(
        description="Scan a directory, filter out .torrent files, and archive them by file size priority using 7z."
    )
    parser.add_argument(
        "directory", 
        type=str, 
        help="Path to the target directory to scan (depth 1)"
    )
    args = parser.parse_args()
    
    target_dir = os.path.abspath(args.directory)
    
    if not os.path.isdir(target_dir):
        logging.error(f"The provided path is not a valid directory: {target_dir}")
        return

    logging.info(f"Starting directory scan: {target_dir}")

    # 3. Scan Directory (Depth 1 only)
    try:
        all_items = os.listdir(target_dir)
    except Exception as e:
        logging.error(f"Failed to read directory {target_dir}: {e}")
        return

    # Filter out directories and *.torrent files, collect file sizes
    filtered_files = []
    for item in all_items:
        item_path = os.path.join(target_dir, item)
        if os.path.isfile(item_path) and not item.lower().endswith('.torrent'):
            try:
                file_size = os.path.getsize(item_path)
                filtered_files.append((item_path, file_size))
            except Exception as e:
                logging.warning(f"Could not read file size for {item}: {e}")

    if not filtered_files:
        logging.info("No matching files found to back up (skipping folders and .torrent files).")
        return

    # Sort files by priority: smallest file size first
    filtered_files.sort(key=lambda x: x[1])
    logging.info(f"Found {len(filtered_files)} files. Sorted by smallest size first.")

    # 4. Create Timestamped Temporary Subdirectory
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    temp_folder_name = f"backup-{timestamp}"
    temp_folder_path = os.path.join(target_dir, temp_folder_name)
    
    try:
        os.makedirs(temp_folder_path, exist_ok=True)
        logging.info(f"Created temporary directory: {temp_folder_path}")
    except Exception as e:
        logging.error(f"Failed to create temporary staging folder: {e}")
        return

    # 5. Copy Filtered Files in Order of Size Priority
    for file_path, size in filtered_files:
        try:
            shutil.copy2(file_path, temp_folder_path)
            logging.info(f"Copied ({size} bytes): {os.path.basename(file_path)}")
        except Exception as e:
            logging.error(f"Failed to copy file {file_path}: {e}")

    # 6. Ensure Destination 'backups' Folder Exists
    backups_dest_dir = os.path.join(target_dir, "backups")
    try:
        os.makedirs(backups_dest_dir, exist_ok=True)
        logging.info(f"Destination folder validated: {backups_dest_dir}")
    except Exception as e:
        logging.error(f"Failed to create destination 'backups' folder: {e}")
        shutil.rmtree(temp_folder_path, ignore_errors=True)
        return

    # 7. Compress the Temp Folder via Subprocess
    archive_name = f"{temp_folder_name}.7z"
    archive_path = os.path.join(backups_dest_dir, archive_name)
    
    logging.info(f"Executing native shell compression via {seven_zip_cmd}...")
    
    cmd = [seven_zip_cmd, "a", "-m0=lzma2", "-mx=9", "-mfb=273", "-md=64m", "-ms=on", archive_path, temp_folder_path]
    
    try:
        # Executes command, captures stdout/stderr streams cleanly without printing raw text to console
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True)
        logging.info("7z compression completed successfully.")
        logging.debug(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"7z process failed. Tool error message:\n{e.stdout}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during shell execution: {e}")
    finally:
        # 8. Clean up temporary staging directory
        logging.info(f"Cleaning up temporary folder: {temp_folder_path}")
        shutil.rmtree(temp_folder_path, ignore_errors=True)

    logging.info("Backup workflow finished.")

if __name__ == "__main__":
    main()
