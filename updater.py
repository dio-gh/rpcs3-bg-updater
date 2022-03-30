import requests
import subprocess
import re
import os

LOCAL_COMMIT_HASH = '4a86638c'

UPDATE_API_ENDPOINT = 'https://update.rpcs3.net'
UPDATE_API_VERSION_ID = 'v2'

def update_commit_hash(new_commit_hash):
    with open(os.path.basename(__file__), 'r+') as script:
        line = script.read()
        line = re.sub(r"(LOCAL_COMMIT_HASH = )'[0-9a-fA-F]{8}'", f"\\1'{new_commit_hash}'", line)
        script.seek(0)
        script.write(line)
        script.truncate()

os.chdir(os.path.dirname(__file__))

# example url: https://update.rpcs3.net/?api=v2&c=42aa8f26
api_response = requests.get(UPDATE_API_ENDPOINT, params={'api': UPDATE_API_VERSION_ID, 'c': LOCAL_COMMIT_HASH}).json()

# 'return_code' is set to 1 if the client should retrieve the latest update, 0 otherwise
if api_response["return_code"] > 0:
    print("Update found!")

    # print version identifiers
    print("Current version: " + api_response["current_build"]["version"])
    print("Latest version: " + api_response["latest_build"]["version"])

    print("Downloading update...")

    update_blob = requests.get(api_response["latest_build"]["windows"]["download"])
    update_filename = re.findall('filename=(.+)', update_blob.headers.get('content-disposition'))[0]
    open(update_filename, 'wb').write(update_blob.content)

    # 7z x -y -o"outdir" <filename>
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    extraction_proc = subprocess.Popen(['7z', 'x', '-y', update_filename], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, startupinfo=si, shell=True)
    extraction_status = extraction_proc.wait()
    #extraction_status = os.system('7z x -y ' + update_filename)
    os.remove(update_filename)

    # update commit hash in the script if everything succeeded
    if extraction_status == 0:
        update_commit_hash(re.findall('[0-9a-fA-F]{8}', update_filename)[0])
        print("Updating finished, exiting...")
    else:
        print("An error has occured while updating. Retrying later...")

else:
    print("No updates found!")
    print("Version identifier: " + api_response["latest_build"]["version"])
    print("Exiting...")