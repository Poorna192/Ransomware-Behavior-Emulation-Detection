Advanced Ransomware Emulation & Detection Lab
This project is an educational tool designed to simulate a multi-stage ransomware attack chain within a controlled virtual lab. It serves as a practical exercise for cybersecurity students, analysts, and enthusiasts to understand and detect modern attacker tactics, techniques, and procedures (TTPs) using industry-standard open-source tools.


⚠️ Disclaimer
This tool is for educational and security research purposes only. The scripts and techniques described should only be used in a dedicated, isolated, and non-critical lab environment like a Virtual Machine. The author is not responsible for any misuse or damage caused by this tool.

Project Overview
This project consists of two main components:

A Sophisticated Ransomware Emulator: A Python-based tool (ransomware_emulator.py) designed to be packaged into a standalone executable that mimics the behavior of a real-world ransomware attack.

A Multi-Layered Detection Strategy: A methodology (ransomware_detector_unified.py) for using professional security tools (Wireshark, Sysinternals Suite) to detect each stage of the simulated attack.

Emulator Features (The Attacker's TTPs)
The emulator was iteratively developed to simulate the following TTPs in a realistic attack chain:

Network C2 Communication: Simulates a "call home" to a command-and-control server via DNS and HTTP requests.

Data Exfiltration: Identifies "sensitive" documents (.docx, .xlsx), copies them to a hidden staging directory in the %TEMP% folder, and simulates an upload to the C2 server.

Privilege Escalation: The script can be run with elevated privileges to unlock its full destructive potential. A version was successfully tested that triggered a UAC prompt to self-elevate.

Persistence: Establishes a foothold on the system by creating a startup key in the HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run path in the Windows Registry.

Anti-Recovery Measures: Attempts to delete Volume Shadow Copies using the vssadmin.exe command to prevent easy file recovery (this action requires Administrator privileges to succeed).

Impact: Renames and simulates the encryption of user files with a dynamically generated random extension and creates a ransom note.

Obfuscation: The final script was successfully packaged into a standalone .exe using PyInstaller to simulate a real-world malware executable.

Detection Strategy (The Defender's Playbook)
A comprehensive, defense-in-depth strategy was developed and validated, using the right professional tool to find the evidence for each specific behavior:

Network Analysis (Wireshark):

Detection: Successfully captured and filtered live network traffic to isolate the malicious DNS query for the C2 server and the subsequent HTTP POST request for data exfiltration.

Endpoint Forensic Analysis (Sysinternals Suite):

Detecting Persistence (Autoruns): Successfully identified the malicious registry key created by the emulator in the "Logon" tab, providing clear evidence of the persistence mechanism.

Detecting Anti-Recovery (Process Monitor): Successfully configured ProcMon with administrator rights to capture the ephemeral evidence of the emulator launching the vssadmin.exe process, a critical Indicator of Attack.

Real-time File System Monitoring (Python Watchdog):

Detection: Developed a custom Python detector script with a "Canary File" (CANARY_DO_NOT_TOUCH.txt). This heuristic-based approach proved highly effective at detecting the file encryption stage, even when the attacker used stealth and randomization techniques.

How to Set Up and Run This Project
Environment: Set up a dedicated Windows 10 Virtual Machine (e.g., using VirtualBox) and disable Windows Defender to prevent interference.

Dependencies: Install Python 3 on the VM and the required libraries: pip install requests pyinstaller.

Run the Emulator:

To run as a standard user, simply run python ransomware_emulator.py from a standard command prompt.

To run with full capabilities (e.g., to make vssadmin succeed), right-click the command prompt and select "Run as administrator" before running the script.

Detection: Use the ransomware_detector_unified.py playbook as a guide to set up Wireshark, Autoruns, and Process Monitor to observe the attack in real-time.
