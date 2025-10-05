# Installation Guide for CTA Evaluation System

This guide provides detailed installation instructions for different operating systems and user levels.

> **⚡ Quick Start**: Already have Python installed? Check [QUICKSTART.md](QUICKSTART.md) for the fastest setup!

## Table of Contents
- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [Detailed Installation](#detailed-installation)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Troubleshooting](#troubleshooting)
- [Verification](#verification)

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **RAM**: 4GB (8GB recommended)
- **Storage**: 500MB free space
- **Internet**: Required for LLM API calls

### Required Accounts
- **OpenAI Account**: You need an OpenAI API key
  - Sign up at: https://platform.openai.com/signup
  - Get API key at: https://platform.openai.com/api-keys

---

## Quick Installation

For experienced users with Python already installed:

```bash
# Clone the repository
git clone https://github.com/halilokur91/cta-evaluation-system.git
cd cta-evaluation-system

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## Detailed Installation

### Windows

#### Step 1: Install Python

1. **Download Python**:
   - Visit https://www.python.org/downloads/
   - Download Python 3.8 or higher (recommended: Python 3.11)
   - **Important**: During installation, check ✅ "Add Python to PATH"

2. **Verify Installation**:
   ```cmd
   python --version
   pip --version
   ```
   If you see version numbers, Python is installed correctly.

#### Step 2: Download the Project

**Option A: Using Git**
```cmd
# Install Git from https://git-scm.com/download/win if not installed
git clone https://github.com/halilokur91/cta-evaluation-system.git
cd cta-evaluation-system
```

**Option B: Direct Download**
1. Go to https://github.com/halilokur91/cta-evaluation-system
2. Click green "Code" button → "Download ZIP"
3. Extract the ZIP file
4. Open Command Prompt in the extracted folder

#### Step 3: Create Virtual Environment (Recommended)

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) at the beginning of your command prompt
```

#### Step 4: Install Dependencies

```cmd
# Upgrade pip first
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

#### Step 5: Configure API Key

1. Open the application:
   ```cmd
   python main.py
   ```

2. Go to **⚙️ Settings** tab
3. Enter your OpenAI API key
4. Select model (recommended: `gpt-4o`)
5. Click **Save Settings**

---

### macOS

#### Step 1: Install Python

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11
```

**Option B: Official Installer**
1. Download from https://www.python.org/downloads/macos/
2. Install the .pkg file
3. Follow installation wizard

#### Step 2: Download the Project

```bash
# Install Git if needed
brew install git

# Clone repository
git clone https://github.com/halilokur91/cta-evaluation-system.git
cd cta-evaluation-system
```

#### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

#### Step 5: Install Tkinter (if needed)

If you get tkinter errors:
```bash
brew install python-tk@3.11
```

#### Step 6: Run Application

```bash
python main.py
```

---

### Linux

#### Step 1: Install Python and Dependencies

**Ubuntu/Debian:**
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv python3-tk

# Install Git
sudo apt install git
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-pip python3-tkinter git
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip tk git
```

#### Step 2: Clone Repository

```bash
git clone https://github.com/halilokur91/cta-evaluation-system.git
cd cta-evaluation-system
```

#### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

#### Step 5: Run Application

```bash
python main.py
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "python is not recognized as a command"

**Solution (Windows)**:
1. Reinstall Python and check "Add Python to PATH"
2. Or manually add Python to PATH:
   - Search for "Environment Variables" in Windows
   - Edit PATH variable
   - Add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311`

**Solution (macOS/Linux)**:
Use `python3` instead of `python`:
```bash
python3 main.py
```

#### Issue 2: "No module named 'tkinter'"

**Windows**: Reinstall Python and ensure "tcl/tk and IDLE" is checked

**macOS**:
```bash
brew install python-tk@3.11
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt install python3-tk
```

#### Issue 3: "ModuleNotFoundError: No module named 'customtkinter'"

**Solution**:
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt

# Or install individually:
pip install customtkinter
```

#### Issue 4: "Permission Denied" errors

**Solution**:
```bash
# Don't use sudo with pip
# Instead, use virtual environment:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue 5: OpenAI API Key errors

**Solution**:
1. Verify your API key at https://platform.openai.com/api-keys
2. Check your API credits/billing at https://platform.openai.com/account/billing
3. Ensure the key starts with `sk-`
4. Try generating a new key if problems persist

#### Issue 6: Slow Installation on Windows

**Solution**:
```cmd
# Use pip with increased timeout
pip install --default-timeout=100 -r requirements.txt

# Or install packages one by one
pip install customtkinter
pip install openai
# ... etc
```

#### Issue 7: "SSL Certificate Verify Failed"

**Solution**:
```bash
# Upgrade pip and certifi
pip install --upgrade pip certifi

# If still failing (temporary workaround):
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

---

## Verification

### Test Your Installation

1. **Check Python version**:
   ```bash
   python --version  # Should show 3.8 or higher
   ```

2. **Check installed packages**:
   ```bash
   pip list
   ```
   Verify these packages are installed:
   - customtkinter
   - openai
   - pandas
   - matplotlib
   - reportlab

3. **Run the application**:
   ```bash
   python main.py
   ```
   The GUI should open without errors.

4. **Test API connection**:
   - Go to Settings tab
   - Enter API key
   - Try a simple transliteration

---

## For Beginners: Complete Walkthrough

### If you've never installed Python before:

#### Windows Users:
1. **Download Python**: Go to python.org, download latest version
2. **Install**: Run installer, check "Add Python to PATH" ✅
3. **Open Command Prompt**: Press `Win + R`, type `cmd`, press Enter
4. **Follow Step 2-5** in the Windows section above

#### macOS Users:
1. **Open Terminal**: Press `Cmd + Space`, type "terminal", press Enter
2. **Install Homebrew**: Copy-paste the command from homebrew.sh
3. **Install Python**: Type `brew install python`
4. **Follow Step 2-6** in the macOS section above

#### Linux Users:
1. **Open Terminal**: Usually `Ctrl + Alt + T`
2. **Install Python**: Use your distribution's package manager (see Step 1 above)
3. **Follow Step 2-5** in the Linux section above

---

## Video Tutorials

For visual learners, consider watching:
- "Python Installation for Beginners" on YouTube
- "Virtual Environments in Python" tutorials
- "Git Basics for Beginners"

---

## Getting Help

If you encounter issues not covered here:

1. **Check GitHub Issues**: https://github.com/halilokur91/cta-evaluation-system/issues
2. **Create New Issue**: Provide:
   - Your operating system and version
   - Python version (`python --version`)
   - Error message (full text)
   - Steps you followed

---

## Next Steps

After successful installation:
1. Read [USER_GUIDE.md](USER_GUIDE.md) for usage instructions
2. Set up your OpenAI API key in Settings
3. Try the sample workflows in the Module Introduction tab
4. Explore each module's functionality

---

**Last Updated**: 2024
**Version**: 1.0
**Support**: hibrahim.okur@iste.edu.tr

