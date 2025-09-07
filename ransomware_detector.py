# ransomware_detector_unified.py (Industry Methodology Playbook)

import os
import time

def print_header(title):
    """Prints a formatted header."""
    print("\n" + "="*60)
    print(f"### {title.upper()} ###")
    print("="*60)

def detection_layer_1_network():
    """Instructions for detecting network-based indicators."""
    print_header("Detection Layer 1: Network C2 Communication")
    print("This layer detects the malware's attempt to 'call home'.")
    print("\nTool to Use: Wireshark")
    print("\n--- Detection Steps ---")
    print("1. Run Wireshark as an Administrator.")
    print("2. Start a live capture on your main network interface (e.g., 'Ethernet0').")
    print("3. In the 'Apply a display filter...' bar, enter the following filter and press Enter:")
    print('   -> dns.qry.name contains "ransomware-c2" or http.request.method == "POST"')
    print("\n--- What to Look For ---")
    print("You will see two key events:")
    print("  A) A DNS query for the fake C2 server domain.")
    print("  B) An HTTP POST request, which is the simulated data exfiltration upload.")
    time.sleep(2)

def detection_layer_2_persistence():
    """Instructions for detecting persistence mechanisms."""
    print_header("Detection Layer 2: Persistence Mechanism")
    print("This layer detects the malware trying to survive a reboot.")
    print("\nTool to Use: Microsoft Autoruns")
    print("\n--- Detection Steps ---")
    print("1. Run Autoruns.exe as an Administrator.")
    print("2. After the initial scan, click on the 'Logon' tab.")
    print("\n--- What to Look For ---")
    print("  -> A new, highlighted entry (usually yellow) for the malicious application.")
    print("     The 'Image Path' will point directly to your emulator script or EXE.")
    time.sleep(2)

def detection_layer_3_anti_recovery():
    """Instructions for detecting attempts to delete backups."""
    print_header("Detection Layer 3: Anti-Recovery & Defense Evasion")
    print("This layer detects the malware trying to delete system backups.")
    print("\nTool to Use: Microsoft Process Monitor (ProcMon)")
    print("\n--- Detection Steps ---")
    print("1. Run Procmon.exe as an Administrator.")
    print("2. Go to Filter -> Filter... and click 'Reset'.")
    print("3. Add this single, high-fidelity filter:")
    print("   -> 'Process Name' -- 'is' -- 'vssadmin.exe' -- then 'Include'")
    print("4. Click OK and clear the display (Ctrl+X).")
    print("\n--- What to Look For ---")
    print("  -> The moment the emulator runs, the 'vssadmin.exe' process will appear in the log.")
    print("     This is a critical indicator of a ransomware attack.")
    time.sleep(2)

def detection_layer_4_file_system():
    """Instructions for detecting the final file encryption stage."""
    print_header("Detection Layer 4: File System Anomalies (Canary File)")
    print("This final layer detects the actual file encryption activity.")
    print("\nTool to Use: Our original Canary File detector script")
    print("\n--- Detection Steps ---")
    print("1. Run the Canary File detector script from a separate command prompt.")
    print("2. It will create a 'CANARY_DO_NOT_TOUCH.txt' file.")
    print("\n--- What to Look For ---")
    print("  -> A 'RANSOMWARE ALERT!' will be triggered the moment the emulator renames")
    print("     or modifies the canary file.")
    time.sleep(2)


if __name__ == "__main__":
    print_header("Unified Ransomware Detection Strategy")
    print("This playbook outlines a multi-layered defense to detect the advanced emulator.")
    print("Run the emulator, then use the tools below to find the forensic evidence.")
    
    detection_layer_1_network()
    detection_layer_2_persistence()
    detection_layer_3_anti_recovery()
    detection_layer_4_file_system()
    
    print("\n" + "="*60)
    print("### DETECTION PLAYBOOK COMPLETE ###")
    print("="*60)