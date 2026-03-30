# 🚀 Installation Guide

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/LX1309244704/weiyuan.git
cd weiyuan
```

### 2. Install Basic Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Optional Dependencies (Choose what you need)

#### For RPA Features
```bash
pip install -r requirements_rpa.txt
```

#### For PC Client GUI
```bash
pip install -r requirements_gui.txt
```

### 4. Configuration

Copy the example environment file and configure:

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Verify Installation

```bash
python -m rpa --help
```

---

## Detailed Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) Node.js 16+ for Lark CLI

### Step-by-Step Installation

#### Step 1: Verify Python Version

```bash
python --version
# Should output: Python 3.8 or higher
```

#### Step 2: Upgrade pip

```bash
pip install --upgrade pip
```

#### Step 3: Install Basic Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Core dependencies (click, requests, yaml, etc.)
- Lark/Feishu SDK
- AI integration (OpenAI, Anthropic)
- Data processing libraries
- Web framework

#### Step 4: Install RPA Dependencies (Optional)

```bash
pip install -r requirements_rpa.txt
```

This installs:
- WeChat plugins (itchat, wechatwork, wechatpy)
- UI automation (pyautogui, selenium)
- OCR (paddleocr, paddlepaddle)
- Web console (flask, flask-socketio)

**Note:** This may take longer to install due to heavy dependencies like PyTorch and PaddlePaddle.

#### Step 5: Install GUI Dependencies (Optional)

```bash
pip install -r requirements_gui.txt
```

This installs:
- PySide6 (Qt framework)
- PyInstaller (for building executables)

#### Step 6: Install Lark CLI (Recommended)

```bash
npm install -g @larksuite/cli
lark-cli auth login --recommend
```

Follow the browser prompt to login with your Lark account.

---

## Troubleshooting

### Issue 1: Encoding Error During Installation

**Problem:**
```
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4...
```

**Solution:**
All requirements files have been fixed to use English comments only. If you still see this error:

```bash
# Set environment variable
export PYTHONIOENCODING=utf-8

# Then install
pip install -r requirements.txt
```

### Issue 2: Permission Denied

**Problem:**
```
Permission denied: '/usr/local/lib/python3.x/...'
```

**Solution:**
```bash
# Use user flag
pip install -r requirements.txt --user

# Or use virtualenv (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Issue 3: Slow Installation

**Problem:**
Installation takes too long, especially for heavy packages.

**Solution:**
```bash
# Use domestic mirror (for China users)
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Or use pip with timeout
pip install -r requirements.txt --timeout 1000
```

### Issue 4: PaddlePaddle Installation Fails

**Problem:**
```
ERROR: Could not find a version that satisfies the requirement paddlepaddle
```

**Solution:**
PaddlePaddle requires specific Python versions and OS. Check official documentation: https://www.paddlepaddle.org.cn/

Alternative: Skip OCR features if not needed.

---

## Verification

After installation, verify:

```bash
# Check RPA core
python -m rpa --help

# Check Lark CLI (if installed)
lark-cli --version

# Test basic import
python -c "import rpa; print('✅ Installation successful!')"
```

---

## Uninstall

```bash
pip uninstall -r requirements.txt -y
pip uninstall -r requirements_rpa.txt -y
pip uninstall -r requirements_gui.txt -y
```

---

## Next Steps

- Read [README.md](README.md) for project overview
- Read [README_RPA.md](README_RPA.md) for RPA usage guide
- Read [README_GUI.md](README_GUI.md) for GUI client guide
- Read [TUTORIAL_WITH_SCREENS.md](docs/TUTORIAL_WITH_SCREENS.md) for detailed tutorials

---

**Need help?** Open an issue on GitHub: https://github.com/LX1309244704/weiyuan/issues
