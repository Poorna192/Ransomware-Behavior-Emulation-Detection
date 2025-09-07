import os
import time

def print_header(title):
    print("\n" + "="*60)
    print(f"### {title.upper()} ###")
    print("="*60)

def detection_layer_1_network():
    print_header("Detection Layer 1: Network C2 Communication")
    print("Detect malware's attempt to 'call home'.")
    print("\nTool: Wireshark")
    print("\nSteps:")
    print("1. Run Wireshark as Administrator.")
    print("2. Start capture on the main network interface (e.g., 'Ethernet0').")
    print("3. Apply this filter:")
    print('   -> dns.qry.name contains "ransomware-c2" or http.request.method == "POST"')
    print("\nIndicators:")
    print("A) DNS queries to fake C2 domains.")
    print("B) HTTP POST requests simulating data exfiltration.")
    time.sleep(2)

def detection_layer_2_persistence():
    print_header("Detection Layer 2: Persistence Mechanism")
    print("Detect attempts to survive reboot.")
    print("\nTool: Microsoft Autoruns")
    print("\nSteps:")
    print("1. Run Autoruns as Administrator.")
    print("2. Click the 'Logon' tab after the scan.")
    print("\nIndicators:")
    print("-> Highlighted entries pointing to the emulator script or EXE.")
    time.sleep(2)

def detection_layer_3_anti_recovery():
    print_header("Detection Layer 3: Anti-Recovery & Defense Evasion")
    print("Detect attempts to delete system backups.")
    print("\nTool: Process Monitor (ProcMon)")
    print("\nSteps:")
    print("1. Run Procmon as Administrator.")
    print("2. Go to Filter -> Filter... and click 'Reset'.")
    print("3. Add this filter:")
    print("   -> 'Process Name' is 'vssadmin.exe' then 'Include'")
    print("4. Clear the display (Ctrl+X).")
    print("\nIndicators:")
    print("-> Appearance of 'vssadmin.exe' process logs when the emulator runs.")
    time.sleep(2)

def detection_layer_4_file_system():
    print_header("Detection Layer 4: File System Anomalies (Canary File)")
    print("Detect file encryption activity.")
    print("\nTool: Canary File Detector Script")
    print("\nSteps:")
    print("1. Run the script from a separate prompt.")
    print("2. A 'CANARY_DO_NOT_TOUCH.txt' file will be created.")
    print("\nIndicators:")
    print("-> 'RANSOMWARE ALERT!' triggers when the canary file is modified or renamed.")
    time.sleep(2)

if __name__ == "__main__":
    print_header("Unified Ransomware Detection Strategy")
    print("Follow this playbook to detect ransomware emulator activity across multiple layers.\n")
    
    detection_layer_1_network()
    detection_layer_2_persistence()
    detection_layer_3_anti_recovery()
    detection_layer_4_file_system()
    
    print("\n" + "="*60)
    print("### DETECTION PLAYBOOK COMPLETE ###")
    print("="*60)
