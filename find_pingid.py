"""Script to find and test PingID application"""
import os
import subprocess
from pywinauto import Application

# Common PingID locations
possible_paths = [
    r"C:\Program Files (x86)\Ping Identity\PingID\PingID.exe",
    r"C:\Program Files\Ping Identity\PingID\PingID.exe",
    r"C:\Users\{}\AppData\Local\Ping Identity\PingID\PingID.exe".format(os.getenv('USERNAME')),
    r"C:\Users\{}\AppData\Roaming\Ping Identity\PingID\PingID.exe".format(os.getenv('USERNAME')),
]

print("Searching for PingID executable...\n")

for path in possible_paths:
    if os.path.exists(path):
        print(f"[FOUND]: {path}")
        print(f"  Testing launch...")
        try:
            app = Application(backend="uia").start(path)
            print(f"  [SUCCESS] Launched!")
            print(f"\n  Listing windows...")
            app.windows()
            break
        except Exception as e:
            print(f"  [FAILED] Launch failed: {e}")
    else:
        print(f"[NOT FOUND]: {path}")

print("\n" + "="*60)
print("Alternative: Check if PingID is running")
print("="*60)

# Try to connect to running PingID
try:
    app = Application(backend="uia").connect(title_re=".*PingID.*", timeout=5)
    print("[SUCCESS] Found running PingID window!")
    windows = app.windows()
    for w in windows:
        print(f"  Window: {w.window_text()}")
except Exception as e:
    print(f"[NOT FOUND] No running PingID window found: {e}")

print("\n" + "="*60)
print("Try using Windows search:")
print("  1. Press Win key and type 'PingID'")
print("  2. Right-click PingID app -> Open file location")
print("  3. Copy the full path and update pingid.py")
print("="*60)