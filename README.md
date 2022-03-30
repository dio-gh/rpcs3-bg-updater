# RPCS3 Background Updater

This is a Python script created for automatically updating RPCS3 in the background, silently. It works by you manually adding it once to the Task Scheduler (on Windows), which will then periodically run it as per your configuration, and keep the emulator up-to-date for you without any interruption.

I believe this to be superior to the currently inbuilt updating methods, as it's operational even when RPCS3 is not running, and does away with all the waiting and bother of updating on startup (which often takes a lot of time for various reasons).

# Requirements:

This script depends on both Python and the `requests` Python library being installed, as well as 7-zip (`7z`) being available on the PATH environment variable.

For installing 7-zip on your system, see [here.](https://www.7-zip.org/download.html)

For installing Python on your system, see [here.](https://www.python.org/downloads/)

For installing the `requests` library using pip, a package manager included with Python:

`pip install requests`

# Usage:

## On Windows:

1. Download the script from GitHub by
  * visiting the script file (`updater.py`) in the repository,
  * clicking on the `Raw` button to display the original file,
  * pressing `CTRL+S` to save it to your RPCS3 installation directory (where `rpcs3.exe` is)

2. Open the Start Menu, then search for and open `Task Scheduler`

3. Click on `Create Task...`

4. Configure the updater task as follows:
  * for `Name`, give it something descriptive, like `RPCS3 Background Updater`
  * on the `Triggers` tab, add a new trigger:
    * for `Begin the task`, select `On Schedule`
    * for frequency, select `One time` (confusing, I know)
    * check the `Repeat task every:` checkbox, and set it to your liking (I use 5 mins)
    * at the `for a duration of:` drop-down, select `Indefinitely`
    * click `OK` to save it
  * on the `Actions` tab, add a new action:
    * for `Action:` you'll want `Start a program`
    * for `Program/script:` you'll want to simply type in `pythonw`
    * for `Add arguments:`, you'll need to provide the path to the script file
      * navigate to your RPCS3 installation directory where you've downloaded it
      * hold `CTRL` and right click
      * select `Copy full path`
      * paste it into the `Add arguments:` textbox (and don't remove the quotes around it)
    * click `OK` to save it
  * on the `Conditions` tab, check the `only if network connection is available` (optional)
  * click `OK` to finalize the task

5. Open RPCS3, and in `Config` > `GUI` change the `Check for updates on startup` setting to `Background`

If you've done everything correctly, you'll no longer be prompted to update RPCS3 on startup, nor will it forcefully update on every launch. Instead, the emulator will be kept up-to-date by this script, periodically polling for updates, and applying them as they come, seamlessly.

## On Unix:

The script won't work on Unix-like systems right now. Wouldn't take much to fix it, but I have no desire to. PRs welcome, though this way of manhandling the lifecycle management is a very Windows problem, so I can't imagine there to be much interest to replicate it for AppImages.

# Notes and limitations

This script will only work as long as the specific version (`v2`) of their update API endpoint does, but that seems to be stable, so should be fine for quite some time.

The script also utilizes the `shell=True` flag when invoking 7-zip via `subprocess.Popen()`, which has security implications. Too bad I haven't bothered to read up on those, eh?

Oh yeah, there's basically no error checking either - if something fails, it doesn't matter much, since it's periodically re-tried anyways. Shouldn't trash the storage at the very least... I think.