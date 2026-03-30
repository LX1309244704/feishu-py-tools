# 🚀 Quick Installation Guide - Step by Step

## Option 1: Minimal Installation (Recommended for Beginners)

### Step 1: Install Core Dependencies Only

```bash
pip install click requests python-dotenv pyyaml rich jsonschema jinja2 python-dateutil pytz
```

### Step 2: Verify Installation

```bash
python -m rpa --help
```

### Step 3: You're Ready!

Now you can:
- Create RPA flows
- Use YAML/JSON format
- Run basic automations

---

## Option 2: Standard Installation (Most Features)

### Step 1: Install Minimal Dependencies

```bash
pip install click requests python-dotenv pyyaml rich jsonschema jinja2 python-dateutil pytz
```

### Step 2: Install Feishu SDK

```bash
pip install lark-oapi
```

### Step 3: Install Web Console Dependencies

```bash
pip install flask gunicorn apscheduler
```

### Step 4: Verify Installation

```bash
python -m rpa --help
```

---

## Option 3: Full Installation (All Features)

### Step 1: Install Core Dependencies

```bash
pip install click requests python-dotenv pyyaml rich jsonschema jinja2 python-dateutil pytz
```

### Step 2: Install Feishu SDK

```bash
pip install lark-oapi
```

### Step 3: Install Web Console

```bash
pip install flask gunicorn apscheduler
```

### Step 4: Install Data Processing (Optional)

```bash
pip install pandas numpy matplotlib
```

### Step 5: Install AI Integration (Optional)

```bash
pip install openai anthropic
```

### Step 6: Install Lark CLI (Optional, needs Node.js)

```bash
npm install -g @larksuite/cli
lark-cli auth login --recommend
```

---

## Common Installation Issues and Solutions

### Issue: Package Not Found

**Problem:**
```
ERROR: Could not find a version that satisfies the requirement XXX
```

**Solution:**
1. Check if the package name is correct
2. Some packages are in the Python standard library (like `concurrent.futures`)
3. Skip optional features you don't need

### Issue: Slow Installation

**Solution:**
```bash
# Use a faster mirror
pip install click requests -i https://pypi.tuna.tsinghua.edu.cn/simple

# Or increase timeout
pip install click requests --timeout 300
```

### Issue: Permission Denied

**Solution:**
```bash
# Use --user flag
pip install click requests --user

# Or use virtualenv (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install click requests
```

---

## What Each Package Does

### Core (Required)
- `click` - CLI framework
- `requests` - HTTP requests
- `python-dotenv` - Environment variables
- `pyyaml` - YAML parsing
- `rich` - Terminal formatting
- `jsonschema` - Schema validation
- `jinja2` - Template engine
- `python-dateutil` - Date handling
- `pytz` - Timezone handling

### Feishu Integration
- `lark-oapi` - Lark/Feishu SDK

### Web Console
- `flask` - Web framework
- `gunicorn` - WSGI server
- `apscheduler` - Task scheduling

### Data Processing (Optional)
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `matplotlib` - Plotting

### AI Integration (Optional)
- `openai` - OpenAI API
- `anthropic` - Anthropic Claude API

---

## Verification Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(click|requests|pyyaml|lark)"

# Test import
python -c "import rpa; print('✅ Installation successful!')"
```

---

## Next Steps

After installation:

1. **Read the documentation:**
   - [README.md](README.md) - Project overview
   - [TUTORIAL_WITH_SCREENS.md](docs/TUTORIAL_WITH_SCREENS.md) - Detailed tutorial

2. **Create your first flow:**
   ```bash
   python -m rpa init my-first-flow
   ```

3. **Run a flow:**
   ```bash
   python -m rpa run my-first-flow.yaml
   ```

4. **Start the web console (optional):**
   ```bash
   python -m rpa web
   # Open http://localhost:8888
   ```

---

## Need Help?

- Open an issue: https://github.com/LX1309244704/weiyuan/issues
- Read troubleshooting in [INSTALLATION.md](INSTALLATION.md)
- Check existing issues and discussions
