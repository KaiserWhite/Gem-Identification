# Gem Identification Toolkit

This project simulates the process of hiring a gemcutter, identifying gems, and optionally cutting them. It includes a point-and-click desktop app (built with Tkinter) and an interactive command-line version. You can use it to quickly generate gems for tabletop games or other creative projects.

## 1. What you need

* A computer running Windows 10/11, macOS, or a modern Linux distribution.
* **Python 3.10 or newer.** The program only uses the standard library, so there are no extra packages to install. Tkinter ships with the regular Python installers for Windows and macOS. Most Linux distributions include it by default.

> **Tip for Windows users:** During the Python installation make sure the option **"Add Python 3.x to PATH"** is checked. This lets you run `python` from the Command Prompt without extra steps.

## 2. Install Python

Follow the instructions for your operating system. If Python is already installed you can skip this section.

### Windows

1. Visit [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/).
2. Click the latest "Download Python 3.x" button.
3. Run the downloaded installer.
4. On the first screen, **check the box** labeled **"Add Python 3.x to PATH"**.
5. Click **Install Now** and wait for the setup to finish.

### macOS

1. Visit [https://www.python.org/downloads/macos/](https://www.python.org/downloads/macos/).
2. Download the latest macOS installer package (`.pkg`).
3. Double-click the downloaded file and follow the prompts.

### Linux

Most distributions include Python 3 by default. To install or upgrade Python 3 and Tkinter, use your package manager. Examples:

* **Ubuntu/Debian:** `sudo apt install python3 python3-tk`
* **Fedora:** `sudo dnf install python3 python3-tkinter`

## 3. Download the project files

Choose either the zip download or Git clone method:

### Option A: Download the ZIP (easiest)

1. Open the project page in your browser.
2. Click the **Code** button and choose **Download ZIP**.
3. When the download finishes, right-click the ZIP file and choose **Extract All…** (Windows) or double-click to unzip (macOS/Linux).
4. Remember the folder where you extracted the files (for example, `Downloads\Gem-Identification-main`).

### Option B: Use Git (for users familiar with Git)

```bash
git clone https://github.com/<your-account>/Gem-Identification.git
cd Gem-Identification
```

## 4. Verify Python is ready

Open a terminal window:

* **Windows:** Press <kbd>Win</kbd> + <kbd>R</kbd>, type `cmd`, and press Enter.
* **macOS:** Open **Terminal** from Applications → Utilities.
* **Linux:** Open your preferred terminal emulator.

Type the following command and press Enter:

```bash
python --version
```

If this prints something like `Python 3.11.6`, you are ready to go. If you get an error such as "'python' is not recognized", close the window and reopen it. If the error remains, reinstall Python and make sure you checked "Add Python to PATH" during setup.

> On some macOS and Linux systems you may need to use `python3` instead of `python`. All commands in this guide work with either name.

## 5. Run the graphical app (recommended)

1. Use `cd` to change into the folder where you extracted the project. For example:

   ```bash
   cd "C:\\Users\\YourName\\Downloads\\Gem-Identification-main"
   ```

   Replace the path with the location on your computer.

2. Start the GUI by running:

   ```bash
   python launch_gui.py
   ```

3. The "Gem Identification & Cutting" window will open. You can now hire retainers, configure gem batches, roll results, and review the output using the tabs in the interface.

If double-clicking is more comfortable, you can also double-click `launch_gui.py` in File Explorer/Finder. A console window will appear and the GUI will launch. If the window closes immediately, reopen a terminal and run the command manually to see any error messages.

## 6. Use the command-line version (optional)

The project also includes a text-based workflow inside `gem_calculator_v15.py`.

```bash
python gem_calculator_v15.py
```

Follow the prompts to select retainer details, gem categories, and cutting options directly in the terminal.

## 7. Troubleshooting

* **"python" not found:** Re-run the Python installer and ensure "Add Python to PATH" is checked (Windows) or use `python3` (macOS/Linux).
* **Tkinter missing (Linux):** Install the `python3-tk` package using your package manager, then try again.
* **Permission issues:** If your computer blocks files from the internet, right-click the ZIP file, choose **Properties**, and click **Unblock** before extracting (Windows only).

## 8. Updating to a newer version

If you downloaded the ZIP, repeat the download steps and replace your old folder with the new one. If you used Git, run:

```bash
git pull
```

## 9. Need more help?

If you run into a problem that these steps do not cover, take a screenshot of any error message and share it with the maintainer or community where you found this project. Knowing the exact wording of the error and which step you were on will make it easier to help.
