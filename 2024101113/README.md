# DASS Assignment 2 Submission

## GitHub Repository
https://github.com/your-username/dass-assignment-2

> **Note:** Replace the URL above with your actual GitHub repository link before submission.

---

## Folder Structure

```
2024101113/
├── whitebox/
│   ├── diagrams/        ← CFG hand-drawn image (cfg.png)
│   ├── tests/           ← pytest white-box test files
│   ├── code/            ← MoneyPoly source code (moneypoly package)
│   ├── report.md
│   └── report.pdf
├── integration/
│   ├── diagrams/        ← Call Graph hand-drawn image (call_graph.png)
│   ├── tests/           ← pytest integration test file
│   ├── code/            ← StreetRace Manager modules
│   ├── report.md
│   └── report.pdf
├── blackbox/
│   ├── tests/           ← pytest API test file (requires server on localhost:8080)
│   ├── report.md
│   └── report.pdf
└── README.md
```

---

## Running the Tests and Code

### 1. White Box Testing (MoneyPoly)

**Run the game interactively:**
```bash
# From the root 2024101113/ directory
python whitebox/code/main.py
```

**Run the white-box pytest test suite:**
```powershell
# PowerShell (Windows)
$env:PYTHONPATH = "whitebox/code"
python -m pytest whitebox/tests -v
```
```bash
# Linux / macOS
PYTHONPATH=whitebox/code python -m pytest whitebox/tests -v
```

---

### 2. Integration Testing (StreetRace Manager)

**Run the integration tests:**
```powershell
# PowerShell (Windows) – run from the root 2024ABCD/ directory
$env:PYTHONPATH = "integration/code"
python -m pytest integration/tests -v
```
```bash
# Linux / macOS
PYTHONPATH=integration/code python -m pytest integration/tests -v
```

> **Important:** Do NOT set `PYTHONPATH` to just `"code"` from inside the `integration/` folder — the
> directory name `code` conflicts with Python's standard-library `code` module. Always use the full
> relative path `integration/code` from the project root, or the absolute path to `integration/code/`.

---

### 3. Black Box Testing (QuickCart API)

**Start the QuickCart server (Docker required):**
```bash
docker load -i quickcart_image.tar
docker run -d -p 8080:8080 quickcart
```

**Run the black-box pytest suite:**
```bash
# Tests auto-skip gracefully when no server is reachable
python -m pytest blackbox/tests/test_api.py -v
```

> Tests that require the live server are decorated with `@skip_if_no_server` and will be marked
> **SKIPPED** (not FAILED) when the Docker container is not running.

---

## Diagrams

| Section | File | Status |
|---------|------|--------|
| White Box CFG | `whitebox/diagrams/cfg.png` | Hand-drawn, to be scanned and placed here |
| Integration Call Graph | `integration/diagrams/call_graph.png` | Hand-drawn, to be scanned and placed here |

---

## Git Commit History (Summary)

| Commit | Message |
|--------|---------|
| Initial commit | Baseline MoneyPoly code |
| Iteration 1 | Add missing docstrings |
| Iteration 2 | Remove unused imports and variables |
| Iteration 3 | Fix syntax issues |
| Iteration 4 | Fix bare excepts, initialize variables |
| Iteration 5 | Resolved too-many-instance-attributes in Player by extracting JailState dataclass |
| Iteration 6 | Resolved too-many-branches and too-many-instance-attributes in Game by extracting Decks, GameEngine, and handler dictionaries |
| Iteration 7 | Resolved too-many-arguments and too-many-instance-attributes in Property via PropertyConfig dataclass |
| Error 1 | Fixed bank not deducting loan amounts from its own funds |
| Error 2 | Fixed net_worth() to include property values, not just cash balance |
| Error 3 | Fixed move() to award GO salary when passing (not only landing on) GO |
| Error 4 | Fixed find_winner() using min() instead of max() |
