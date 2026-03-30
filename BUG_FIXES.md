# 🐛 Bug Fixes and Solutions

## Known Issues and Fixes

### Issue 1: GUI Import Error - QLabel not defined

**Error:**
```
File "rpa/gui/pages/flow_page.py", line 104
    left_title = QLabel("<h3>流程列表</h3>")
NameError: name 'QLabel' is not defined
```

**Cause:**
- `QLabel` was used in the code but not imported
- Missing import statement in `rpa/gui/pages/flow_page.py`

**Fix:**
```python
# Before:
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QListWidget, QListWidgetItem, QTextEdit, QPushButton,
    QFileDialog, QMessageBox, QDialog, QFormLayout,
    QLineEdit, QDialogButtonBox, QTabWidget
)

# After:
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QListWidget, QListWidgetItem, QTextEdit, QPushButton,
    QFileDialog, QMessageBox, QDialog, QFormLayout,
    QLineEdit, QDialogButtonBox, QTabWidget, QLabel  # Added QLabel
)
```

**Commit:** `5cd97cb`

---

### Issue 2: Package Not Found - lark-cli-wrapper

**Error:**
```
ERROR: Could not find a version that satisfies the requirement lark-cli-wrapper>=1.0.0
ERROR: No matching distribution found for lark-cli-wrapper>=1.0.0
```

**Cause:**
- `lark-cli-wrapper` does not exist on PyPI
- Official Lark CLI is a Node.js package, not Python

**Fix:**
```python
# Removed from requirements.txt
- lark-cli-wrapper>=1.0.0  # Does not exist

# Use npm instead for official CLI:
npm install -g @larksuite/cli
```

**Commit:** `1eee450`

---

### Issue 3: Package Not Found - concurrent-futures

**Error:**
```
ERROR: Could not find a version that satisfies the requirement concurrent-futures>=3.1.1
ERROR: No matching distribution found for concurrent-futures>=3.1.1
```

**Cause:**
- `concurrent-futures` is part of Python standard library (Python 3.2+)
- Cannot be installed via pip

**Fix:**
```python
# Removed from requirements_rpa.txt
- concurrent-futures>=3.1.1  # Built into Python

# Use directly in code:
from concurrent.futures import ThreadPoolExecutor, as_completed
```

**Commit:** `93a975e`

---

### Issue 4: Encoding Error During Installation

**Error:**
```
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4
```

**Cause:**
- Comments in requirements files were in Chinese
- pip installation failed on some systems

**Fix:**
```python
# Before (Chinese comments):
click>=8.1.0              # CLI框架
requests>=2.31.0           # HTTP请求

# After (English comments):
click>=8.1.0              # CLI framework
requests>=2.31.0           # HTTP requests
```

**Commit:** `d178ae3`

---

### Issue 5: Module Import Errors - Missing Type Annotations

**Error:**
```
NameError: name 'Dict' is not defined
NameError: name 'Any' is not defined
NameError: name 'List' is not defined
NameError: name 'json' is not defined
```

**Cause:**
- Missing type annotation imports
- Missing `json` import

**Fix:**
```python
# rpa/schemas/__init__.py
from typing import Dict, Any  # Added

# rpa/core/variable_engine.py
from typing import Dict, Any, Optional, List  # Added
import json  # Added

# rpa/core/flow.py
from typing import Dict, Any, Optional, Tuple  # Added
```

**Commit:** `c881b11`

---

## How to Check for Similar Issues

### 1. Verify Imports

```bash
# Find all Python files using GUI widgets
find rpa/gui -name "*.py" -exec grep -l "QLabel" {} \;

# Check if QLabel is imported in each file
grep -r "from.*import.*QLabel" rpa/gui/pages/
```

### 2. Verify Dependencies

```bash
# Test installing requirements file
pip install --dry-run -r requirements.txt

# Check if a package exists
pip search <package-name>  # (may not work on all PyPI mirrors)
# Or visit: https://pypi.org/project/<package-name>/
```

### 3. Test GUI Startup

```bash
# Try to start GUI and check for errors
python start_gui.py 2>&1 | tee gui_startup.log

# Look for NameError or ImportError in log
grep -E "(NameError|ImportError)" gui_startup.log
```

---

## Prevention Tips

### 1. Use Python Standard Library First

Before adding a package to requirements, check if it's in the standard library:
- https://docs.python.org/3/library/index.html

Common built-in modules:
- `concurrent.futures` (not `concurrent-futures`)
- `datetime`, `json`, `os`, `sys`
- `pathlib`, `typing`, `collections`

### 2. Verify Package Existence

Before adding to requirements:
1. Visit https://pypi.org/
2. Search for the package name
3. Check exact spelling (case-sensitive)

### 3. Test Installation Locally

```bash
# Create virtual environment
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Try to install
pip install -r requirements.txt

# If it works, commit changes
```

### 4. Use Minimal Dependencies

- Only add packages you actually need
- Comment optional dependencies
- Create separate files for optional features

---

## Reporting Bugs

If you find a new bug:

1. **Check existing issues:**
   - GitHub Issues: https://github.com/LX1309244704/weiyuan/issues
   - This file for known fixes

2. **Create minimal reproducible example:**
   ```python
   # What code causes the error?
   from rpa.gui.pages.flow_page import FlowPage
   page = FlowPage()
   ```

3. **Include error message:**
   ```
   Traceback (most recent call last):
   ...
   NameError: name 'QLabel' is not defined
   ```

4. **Include system info:**
   ```bash
   python --version
   pip list | grep PySide6
   ```

5. **Submit issue:**
   - Go to https://github.com/LX1309244704/weiyuan/issues/new
   - Fill in the template
   - Attach error log and system info

---

## Status

| Issue | Status | Commit | Fixed In Version |
|-------|--------|--------|------------------|
| GUI Import Error | ✅ Fixed | 5cd97cb | v2.0.0 |
| lark-cli-wrapper | ✅ Fixed | 1eee450 | v2.0.0 |
| concurrent-futures | ✅ Fixed | 93a975e | v2.0.0 |
| Encoding Error | ✅ Fixed | d178ae3 | v2.0.0 |
| Missing Type Annotations | ✅ Fixed | c881b11 | v2.0.0 |

---

## Quick Fix Reference

| Error | Quick Fix |
|-------|-----------|
| `NameError: name 'QLabel' is not defined` | Add `QLabel` to imports |
| `ERROR: Could not find lark-cli-wrapper` | Remove from requirements, use npm |
| `ERROR: Could not find concurrent-futures` | Remove from requirements, it's built-in |
| `UnicodeDecodeError` | Convert comments to English |
| `NameError: name 'Dict'` | Add `from typing import Dict, Any` |

---

**Last Updated:** 2024-03-30  
**Version:** v2.0.0
