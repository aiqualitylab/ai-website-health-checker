# AI Website Health Checker

A simple Python script that checks if a website is up and uses AI to explain any problems.

## Quick Start

1. **Install dependencies:**
```bash
pip install requests markdown python-dotenv openai
```

2. **Add your OpenAI API key** to a `.env` file:
```
OPENAI_API_KEY=sk-your-key-here
```

3. **Run the script:**
```bash
python simple_url_check.py
```

## What It Does

- Checks if a website is accessible
- Shows status: ✅ OK, ⚠️ WARN, or ❌ FAIL
- Uses AI to explain warnings or failures
- Creates `report.md` and `report.html` files

## Configuration

Edit `simple_url_check.py` to change:
- `URL` - website to check
- `TIMEOUT` - how long to wait for response

## Example Output

```
Status: OK
HTTP Code: 200
AI Summary: No issues found.
```
