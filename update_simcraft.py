import requests
import subprocess
import os
import shutil
import urllib

# Get Latest Nightly Version
simcraftURL = "http://downloads.simulationcraft.org/nightly/?C=M;O=D"

downloadPage = requests.get(simcraftURL)

start = downloadPage.text.index('win64')
start = start + downloadPage.text[start:].index('>') + 1
end = start + downloadPage.text[start:].index('</a>')

nightlyFileName = downloadPage.text[start:end]

nightlyVersion = nightlyFileName[nightlyFileName.index('win64') + 6:nightlyFileName.index('.7z')]

print('Latest nightly build: ' + nightlyVersion)

# Get Current Installed Version
installFolder = 'C:\\Users\\Chris\\Downloads\\'
simcraftFolder = installFolder + 'simc-910-01-win64\\'

# Run simc.exe and pull ver from output
output = subprocess.run([simcraftFolder + 'simc.exe'], capture_output=True, text=True).stdout

print (output[:-2])

installedVersion = output[output.index('git build shadowlands ') + 22:output.index(')')] 

print ('Installed Version: ' + installedVersion)

# If Installed < Latest
if(nightlyVersion > installedVersion):
    downloadURL = 'http://downloads.simulationcraft.org/nightly/' + nightlyFileName
    print('Downloading ' + downloadURL)
    urllib.request.urlretrieve(downloadURL, nightlyFileName)

    # Delete old version
    print('Removing old version.')
    shutil.rmtree(simcraftFolder)
    
    # unzip new simcraft 
    print('Extracting new version')
    from pyunpack import Archive
    Archive(nightlyFileName).extractall(installFolder)

    # Delete zip file
    print('Removing 7z file')
    os.remove(nightlyFileName)
else:
    print('Version up to date.')