import pysftp, datetime, py7zr, os, glob
import warnings
from cryptography.fernet import Fernet
warnings.filterwarnings('ignore','.*Failed to load HostKeys.*')

# Change Clinic tablet Number
Tablet_code='Tablet11'

#######################################################################################
# Ensure the following parameters are set appropriately
username = "ugmicdrop_vb"                
remote_File_Path="/" + Tablet_code
# End of parameters
#######################################################################################

# This is the IP address of the ftp server
HOSTNAME = "0f7a55b.netsolhost.com"

# get date and time and put them into a string to apend to the file name
timestr = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

#######################################################################################
# These are the settings for the project
folder_path = "C:/MicDroP/MSAccessDatabase"
myfilename= Tablet_code+'_'+timestr         # File name to upload to server
archive_path = "C:/MicDroP/DailyBackup/"+myfilename+".7z"
# End of settings for project
#######################################################################################

# Use CredFile.ini and key.key to retreive password
# CredFile.ini and key.key were created using writeCredentialsToFile.py
cred_filename = 'C:\\MicDroP\\Scripts\\credfile.ini'
key_file = 'C:\\MicDroP\\Scripts\\keyfile.key'
key = ''


print('Please be patient, this may take a few moments.' + '\n\nBacking up data.....')

with open(key_file,'r') as key_in:
        key = key_in.read().encode()

f = Fernet(key)
with open(cred_filename,'r') as cred_in:
        lines = cred_in.readlines()
        config = {}
        for line in lines:
            tuples = line.rstrip('\n').split('=',1)
            if tuples[0] in ('Password'):
                config[tuples[0]] = tuples[1]
        password = f.decrypt(config['Password'].encode()).decode()

cnOpts = pysftp.CnOpts()            # Connect to the SFTP server
cnOpts.hostkeys = None              # disable host key checking
cnOpts.ciphers = ('aes256-cbc',)    # Set a secure cipher as a tuple

#zip database
with py7zr.SevenZipFile(archive_path, 'w') as archive:
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            archive_file_path = os.path.relpath(file_path, folder_path)
            archive.write(file_path, arcname=archive_file_path)

#Get the lattest zipped file
list_of_files = glob.glob(archive_path) # * means all if need specific format then *.7z
latest_file = max(list_of_files, key=os.path.getctime)

with pysftp.Connection(host=HOSTNAME, username=username, password=password, cnopts=cnOpts) as sftp:
    # change directory
    sftp.cwd(remote_File_Path)

    # Upload file
    sftp.put(latest_file) 
    print('File Successfuly Uploaded.........!') 
