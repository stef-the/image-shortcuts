# image-shortcuts
 Windows and MacOS compatible script to batch replace files with shortcuts for images (or other files) in a directory, using a specified source directory with original files.


### About

This project uses `pypy3.10-7.3.16`, installed and managed using pyenv. It's built using zero external libraries, and with the help of OpenAI's ChatGPT for code commenting, AppleScript and minor optimisations. All other code is handwritten.

At the moment, all of the code is in [main.py](https://github.com/stef-the/image-shortcuts/blob/main/main.py) and can be run without any installs or external libraries (except python), making heavy use of the built-in `os` library.

### How to

- Install a recent version of python3.10 (recommended to use pypy3.10-7.3.16 for speed and compatibility)
- Download [main.py](https://github.com/stef-the/image-shortcuts/blob/main/main.py)
- Configure the program (in main.py, I might implement a different system such as CLI or GUI later on)
- Run the program

### Configuring

Nearly all of the features are accessible through the last 7 lines of the program:

```py
if __name__ == "__main__":
    input_folder = "" # Input/Shortcut folder PATH e.g. "./Images_(Copy)/"
    reference_folder = "" # Reference/Source folder PATH e.g. "./Images/"

    cs0 = ImageTransfer(ile_type="pdf", folder=input_folder)
    print(cs0.exists()) # Checks if
    cs0.convert_image_shortcuts(img_dir=reference_folder)
```

- `input_folder` is the folder in which files will be replaced with shortcuts, if possible. This can be a relative or absolute PATH.
- `reference_folder` is the reference folder from which source files will be pulled for the shortcuts. This can also be a relative or absolute PATH.