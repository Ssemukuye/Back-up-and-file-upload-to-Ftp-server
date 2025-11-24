# Back-up-and-file-upload-to-Ftp-server
Automated Backup & FTP Upload Script
====================================

This script creates a timestamped 7z backup of a local folder and uploads
the newest backup to a remote FTP directory. The FTP password is stored
encrypted and only decrypted during runtime.

------------------------------------
What the Script Does
------------------------------------
1. Builds a timestamped filename for each backup.
2. Compresses a chosen local folder into a .7z archive.
3. Decrypts an encrypted password from disk.
4. Connects to an FTP server using the decrypted password.
5. Uploads the most recent backup file to the remote directory.

------------------------------------
Features
------------------------------------
- Automatic naming using current date and time.
- Folder compression via py7zr.
- Secure password handling with NaCl SecretBox.
- FTP upload using pysftp.
- Designed for Windows paths.
- Finds and uploads the newest backup automatically.

------------------------------------
Requirements
------------------------------------
Install dependencies:

    pip install py7zr pysftp pynacl cryptography

Tested with:
- Python 3.12
- Windows 10/11

------------------------------------
Setup Instructions
------------------------------------
1. Place your encrypted FTP password file at:

   C:\Users\<USER>\Documents\Tess back up\ftp_pwd.txt

2. Adjust these paths in the script if needed:

   folder_path  = C:\micdrop\MSAccessDatabase
   archive_path = C:\Users\TIMO\Documents\back up\dailybackup\
   remote_dir   = /MICD 2025-08-28 03;20;48

3. Make sure MASTER_KEY matches the key used to encrypt the password.

------------------------------------
How to Run
------------------------------------
Run the script:

    python backup_upload.py

The script will:
- Zip the specified folder.
- Save the .7z file to the backup directory.
- Upload the newest backup to the remote FTP server.

------------------------------------
Security Notes
------------------------------------
- The FTP password is never stored in plain text.
- Password is decrypted only at runtime.
- Host key checking is disabled for convenience but can be tightened.
- Keep the master key and encrypted password file secure.

------------------------------------
Limitations
------------------------------------
- Script uses Windows paths by default.
- FTP (not SFTP) does not encrypt file transfers.
- Assumes remote FTP directory already exists.

------------------------------------
License
------------------------------------
This project is available under the MIT License.
Feel free to modify or adapt it for your environment.
