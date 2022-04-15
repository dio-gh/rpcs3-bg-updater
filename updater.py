import requests as req
import subprocess, re, os, winreg

LOCAL_COMMIT = '21f744e2'
SHORTHASH_PATTERN = r'[0-9a-fA-F]{8}'

API_ENDPOINT = 'https://update.rpcs3.net'
API_VER = 'v2'

# example url: https://update.rpcs3.net/?api=v2&c=4a86638c
res = req.get(API_ENDPOINT, params={'api': API_VER, 'c': LOCAL_COMMIT}).json()

# ensure correct working dir
os.chdir(os.path.dirname(__file__))

# set up path to 7-Zip
reg_key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, r'Software\7-Zip')
reg_val, regtype = winreg.QueryValueEx(reg_key, 'Path')
winreg.CloseKey(reg_key)
extractor = reg_val + "7z.exe"

# when the return_code is 1, gotta update
if res["return_code"] == 1:

    # retrieve the update archive
    update_blob = req.get(res["latest_build"]["windows"]["download"])
    update_meta = update_blob.headers.get('content-disposition')
    update_fname = re.findall('filename=(.+)', update_meta)[0]
    open(update_fname, 'wb').write(update_blob.content)

    # extract the update archive
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    extraction_proc = subprocess.Popen(
        [extractor, 'x', '-y', update_fname],
        startupinfo=si,
        shell=True)
    extraction_status = extraction_proc.wait()

    # erase the update archive
    os.remove(update_fname)

    # on success, update the local commit hash based on the update's filename
    if extraction_status == 0:
        with open(os.path.basename(__file__), 'r+') as this_script:
            updated_script = re.sub(
                f"(LOCAL_COMMIT = )'{SHORTHASH_PATTERN}'",
                f"\\1'{re.findall(SHORTHASH_PATTERN, update_fname)[0]}'",
                this_script.read())
            this_script.seek(0)
            this_script.write(updated_script)
            this_script.truncate()