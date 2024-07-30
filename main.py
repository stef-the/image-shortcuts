import os
import subprocess
import platform

def remove_extension(file_path):
    """
    Remove the extension from a file path.

    :param file_path: The path to the file.
    :return: The file path without its extension.
    """
    return os.path.splitext(file_path)[0]

def create_alias_macos(source_file, alias_location):
    """
    Create an alias (shortcut) to a file on macOS.
    
    :param source_file: The path to the original file.
    :param alias_location: The path where the alias should be created.
    """
    source_file_abs = os.path.abspath(source_file)
    alias_location_abs = os.path.abspath(alias_location)
    
    apple_script = f'''
    tell application "Finder"
        make alias file to POSIX file "{source_file_abs}" at POSIX file "{os.path.dirname(alias_location_abs)}"
        set name of result to "{os.path.basename(alias_location_abs)}"
    end tell
    '''
    try:
        subprocess.run(['osascript', '-e', apple_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error creating alias: {e}")
        print(f"AppleScript attempted:\n{apple_script}")

def create_shortcut_windows(source_file, shortcut_location):
    """
    Create a shortcut to a file on Windows.
    
    :param source_file: The path to the original file.
    :param shortcut_location: The path where the shortcut should be created.
    """
    import pythoncom
    from win32com.shell import shell, shellcon
    
    shortcut = pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink, None, pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
    shortcut.SetPath(source_file)
    shortcut.SetWorkingDirectory(os.path.dirname(source_file))
    persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
    persist_file.Save(shortcut_location, 0)

def create_shortcut(source_file, alias_location):
    """
    Create a shortcut to a file, automatically detecting the operating system.
    
    :param source_file: The path to the original file.
    :param alias_location: The path where the alias/shortcut should be created.
    """
    if not os.path.exists(source_file):
        raise FileNotFoundError(f"The source file '{source_file}' does not exist.")
    
    system = platform.system()
    if system == "Darwin":  # macOS
        create_alias_macos(source_file, alias_location)
    elif system == "Windows":
        create_shortcut_windows(source_file, alias_location + ".lnk")
    else:
        raise OSError(f"Unsupported operating system: {system}")

def scan_folder(folder, recursive=False):
    """
    Find all files in folder, with ability to scan subfolders recursively.
    
    :param folder: The folder to scan.
    :param recursive: Whether to scan subfolders.
    :return: List of file paths.
    """
    results = []
    for root, _, files in os.walk(folder):
        for file in files:
            results.append(os.path.join(root, file))
        if not recursive:
            break
    return results

def delete_files_with_same_basename(directory, base_name):
    """
    Delete all files in the specified directory with the same base name.
    
    :param directory: The directory to search in.
    :param base_name: The base name of the files to delete.
    """
    for file in os.listdir(directory):
        if remove_extension(file) == base_name:
            os.remove(os.path.join(directory, file))

class ImageTransfer():
    def __init__(self, path=os.getcwd(), folder=None):
        self.PATH = os.path.abspath(path)
        self.folder = os.path.abspath(folder) if folder else None

    def exists(self):
        return os.path.isdir(self.PATH)

    def convert_image_shortcuts(self, img_dir=os.getcwd(), type_priority=["NEF", "TIF", "TIFF", "JPG", "JPEG"]):
        if not self.folder:
            return False
        if not img_dir:
            img_dir = self.PATH

        img_dir = os.path.abspath(img_dir)
        scanned_folder = scan_folder(img_dir, recursive=True)
        
        priority_map = {ext: idx for idx, ext in enumerate(type_priority)}
        processed_scanned_folder = {}
        
        for file in scanned_folder:
            ext = file.split('.')[-1].upper()
            if ext in priority_map:
                base_name = remove_extension(os.path.basename(file))
                if base_name not in processed_scanned_folder or priority_map[ext] < priority_map[processed_scanned_folder[base_name].split('.')[-1].upper()]:
                    processed_scanned_folder[base_name] = file

        for file in scan_folder(self.folder, recursive=True):
            if file.endswith("DS_Store"):
                continue

            processed_file = remove_extension(os.path.basename(file))

            if processed_file in processed_scanned_folder:
                matching_file = processed_scanned_folder[processed_file]
                ext = matching_file.split('.')[-1].upper()
                matching_files = [matching_file]
                
                # Include .xmp file if it exists for .NEF files
                if ext == 'NEF':
                    xmp_file = remove_extension(matching_file) + ".xmp"
                    if os.path.exists(xmp_file):
                        matching_files.append(xmp_file)
                
                print(f"Matching files found for {file}: {matching_files}")

                # Delete existing files with the same base name
                delete_files_with_same_basename(self.folder, processed_file)
                
                # Create shortcuts for the new files
                for shortcut_source in matching_files:
                    new_file_name = f"{processed_file}.{shortcut_source.split('.')[-1]}"
                    create_shortcut(shortcut_source, os.path.join(self.folder, new_file_name))

if __name__ == "__main__":
    input_folder = "" # Input/Shortcut folder PATH e.g. "./Images_(Copy)/"
    reference_folder = "" # Reference/Source folder PATH e.g. "./Images/"

    cs0 = ImageTransfer(ile_type="pdf", folder=input_folder)
    print(cs0.exists())
    cs0.convert_image_shortcuts(img_dir=reference_folder)