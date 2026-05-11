"""Test PingID launch and window detection"""
from pywinauto import Application
import time

print("Launching PingID...")
app = Application(backend="uia").start(r"C:\Program Files (x86)\Ping Identity\PingID\PingID.exe")

print("Waiting 5 seconds for PingID to fully load...")
time.sleep(5)

print("\n" + "="*60)
print("All application windows:")
print("="*60)
try:
    windows = app.windows()
    for i, window in enumerate(windows):
        print(f"\n[Window {i+1}]")
        print(f"  Title: {window.window_text()}")
        print(f"  Class: {window.class_name()}")
        print(f"  Visible: {window.is_visible()}")
        print(f"  Enabled: {window.is_enabled()}")
except Exception as e:
    print(f"Error getting windows: {e}")

print("\n" + "="*60)
print("Looking for PingID-specific windows...")
print("="*60)

# Try different title patterns
title_patterns = ["PingID", "Ping", "Authentication", "Approve", "Notification"]

for pattern in title_patterns:
    try:
        win = app.window(title_re=f".*{pattern}.*", timeout=2)
        print(f"\n[FOUND] Pattern '{pattern}': {win.window_text()}")

        # Print all controls in this window
        print("  Controls:")
        win.print_control_identifiers()
        break
    except Exception as e:
        print(f"[NOT FOUND] Pattern '{pattern}'")

print("\n" + "="*60)
print("Recommendation:")
print("  Check the window titles above and update pingid.py")
print("  with the correct window title/pattern")
print("="*60)