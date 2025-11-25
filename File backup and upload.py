#import all libraries
from nacl.secret import SecretBox
import base64
import pysftp, datetime, py7zr, os, glob
import warnings
from cryptography.fernet import Fernet
warnings.filterwarnings('ignore','.*Failed to load HostKeys.*')
import time

# set the computer name / code for each machine
computer = 'cpu10'   

# timestamp for naming the backup file
timestamp = time.strftime("%Y_%m_%d-%H-%M-%S")

# build the backup filename with computer id
file_name = f"{computer}_{timestamp}"

# remote directory on the FTP server per computer subfolder
remote_dir = f"/TES/{computer}"

# FTP server login details (password is decrypted later)
HostName = '0f7a55b.netsolhost.com'
UserName = 'ugmicdrop%6423'

# master key used to decrypt the stored password
MASTER_KEY = b"rE6K62GVueu/k3H0vIuPQVh+0hHmwTtnSR+v0F9wsto="

key = base64.b64decode(MASTER_KEY)
box = SecretBox(key)

# read the encrypted password file
with open(r"C:\Users\TIMO\Documents\Tess back up\ftp_pwd.txt", "rb") as f:
    encrypted = base64.b64decode(f.read())

# decrypt the FTP password
password = box.decrypt(encrypted).decode()

print("Decrypted password:", password)

# local folder to back up
folder_path = r"C:\micdrop\MSAccessDatabase"

# location and name of the 7z archive
archive_path = r"C:\Users\TIMO\Documents\back up\dailybackup/" + file_name + ".7z"

print('Please be patient, this may take a few moments.\n\nBacking up data.....')

# build the 7z archive
with py7zr.SevenZipFile(archive_path, 'w') as archive:
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            archive_file_path = os.path.relpath(file_path, folder_path)
            archive.write(file_path, arcname=archive_file_path)

# FTP connection settings
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

# collect matching files into a list
list_of_files = glob.glob(archive_path)

# pick the most recent file based on creation time
latest_file = sorted(list_of_files, key=os.path.getctime)[-1]

# upload the latest backup to the FTP server
with pysftp.Connection(host=HostName, username=UserName, password=password, cnopts=cnopts) as ftp:
    # navigate to the per-computer folder
    with ftp.cd(remote_dir):
        ftp.put(latest_file)

print('File Successfully Uploaded.........!')
