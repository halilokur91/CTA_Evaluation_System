# Quick Start Guide - CTA Evaluation System

This is the fastest way to get started with the CTA Evaluation System.

## ✅ What's Already Done

Your project now has:
- ✅ **Virtual Environment** (`venv/`) - All dependencies isolated
- ✅ **All Requirements Installed** - Ready to use
- ✅ **Launch Scripts** - Easy startup

---

## 🚀 How to Run

### Windows Users

**Option 1: Double-click** (Easiest)
```
Double-click: run.bat
```

**Option 2: Command Line**
```cmd
# Activate virtual environment
venv\Scripts\activate

# Run application
python main.py
```

### macOS/Linux Users

**Option 1: Terminal** (Recommended)
```bash
# Make script executable (first time only)
chmod +x run.sh

# Run
./run.sh
```

**Option 2: Manual**
```bash
# Activate virtual environment
source venv/bin/activate

# Run application
python main.py
```

---

## ⚙️ First Time Setup

When the application opens:

1. **Go to ⚙️ Settings tab**
2. **Enter your OpenAI API Key**
   - Get it from: https://platform.openai.com/api-keys
3. **Select Model**: `gpt-4o` (recommended)
4. **Click**: 💾 Save Settings

---

## 📝 Quick Test

### Test Transliteration

1. **Go to 🔄 Transliteration tab**
2. **Select language**: Turkish
3. **Enter text**:
   ```
   Merhaba dünya. Güzel bir gün.
   ```
4. **Click**: 🚀 TRANSLITERATE
5. **See results** in the right panel

### Test Risk Analysis

1. **Copy the CTA output** from transliteration
2. **Go to ⚠️ Phonetic Risk Analysis tab**
3. **Paste the text**
4. **Click**: 🔍 Run Risk Analysis
5. **View risk table** below

### Test Cognate Alignment

1. **Go to 🔗 Cognate Alignment tab**
2. **Enter words** (one per line):
   ```
   tr:şehir
   az:şəhər
   uz:shahar
   ```
3. **Click**: 🚀 START COGNATE ANALYSIS
4. **View similarity groups**

---

## 📦 Virtual Environment Benefits

Your `venv/` folder contains:
- ✅ **Isolated Python environment** - Doesn't affect system Python
- ✅ **All dependencies** - customtkinter, openai, pandas, matplotlib, etc.
- ✅ **Reproducible** - Same versions everywhere
- ✅ **Clean** - Easy to delete and recreate if needed

---

## 🔄 Updating Dependencies

If you need to update packages:

```bash
# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Update specific package
pip install --upgrade openai

# Update all packages
pip install --upgrade -r requirements.txt
```

---

## 🗑️ Recreating Virtual Environment

If something goes wrong:

```bash
# Delete venv folder
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Recreate
python -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Reinstall
pip install -r requirements.txt
```

---

## 📚 Next Steps

- **Detailed Usage**: See [USER_GUIDE.md](USER_GUIDE.md)
- **Installation Help**: See [INSTALLATION.md](INSTALLATION.md)
- **Features Overview**: See [README.md](README.md)

---

## ❓ Troubleshooting

### "venv not found"
```bash
# Recreate it
python -m venv venv
```

### "Module not found"
```bash
# Activate venv first
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Then reinstall
pip install -r requirements.txt
```

### GUI not opening
```bash
# Check for errors
python main.py
# Read any error messages and check INSTALLATION.md
```

---

**Ready to start!** 🎉

Run: `run.bat` (Windows) or `./run.sh` (macOS/Linux)

