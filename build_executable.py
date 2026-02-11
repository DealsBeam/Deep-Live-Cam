import os
import sys
import shutil
import subprocess
import site

def build_executable():
    print("Starting Deep-Live-Cam Build Process...")

    # 1. Check for PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Please install it with: pip install pyinstaller")
        return

    # 2. Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    entry_point = os.path.join(script_dir, "run.py")

    # 3. Collect Data Files
    # Format: (source, destination)
    added_data = [
        ("modules/*.json", "modules"),
        ("modules/workflow", "modules/workflow"),
        ("locales/*.json", "locales"),
        ("tkinter_fix.py", "."),
    ]

    # 4. Handle customtkinter
    try:
        import customtkinter
        ctk_path = os.path.dirname(customtkinter.__file__)
        added_data.append((ctk_path, "customtkinter"))
    except ImportError:
        print("Warning: customtkinter not found.")

    # 5. Handle onnxruntime and other libraries that might need extra binaries
    # PyInstaller usually handles these via hooks, but we can be explicit if needed.
    # We DON'T manually add the whole onnxruntime directory to avoid conflicts
    # unless specifically needed for certain provider DLLs.

    # 6. Build Command
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile", # Or --onedir if it gets too big
        "--windowed",
        "--name", "Deep-Live-Cam",
        "--icon", "NONE", # Add icon path if available
    ]

    for src, dst in added_data:
        # PyInstaller uses ; on Windows and : on Unix for path separator in --add-data
        sep = ";" if os.name == "nt" else ":"
        cmd.extend(["--add-data", f"{src}{sep}{dst}"])

    # Hidden imports
    hidden_imports = [
        "insightface",
        "onnxruntime",
        "customtkinter",
        "cv2_enumerate_cameras",
        "PIL",
        "psutil",
        "opennsfw2",
        "gfpgan",
        "basicsrs",
    ]

    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])

    cmd.append(entry_point)

    print(f"Running command: {' '.join(cmd)}")

    try:
        subprocess.check_call(cmd)
        print("\nBuild completed successfully!")
        print(f"The executable can be found in the '{os.path.join(script_dir, 'dist')}' folder.")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")

if __name__ == "__main__":
    build_executable()
