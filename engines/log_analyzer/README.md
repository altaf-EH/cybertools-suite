# CyberTools Log Analyzer

A Python-based security log analysis tool for analyzing authentication logs, identifying suspicious login activity, calculating risk indicators, enriching IP information, and generating professional PDF and TXT reports.

CyberTools Log Analyzer is designed for defensive security analysis, security labs, system administrators, SOC/security analysts, and authorized investigations.

---

## Features

### Current Features

- Authentication log analysis
- Failed login attempt detection
- Source IP identification
- Attempt counting and ranking
- Username targeting analysis
- First-seen and last-seen timestamps
- Activity duration analysis
- Risk scoring
- Risk classification
- IP intelligence enrichment
- AbuseIPDB integration
- Professional PDF reports
- TXT report generation
- CyberTools branded reports
- Environment-variable based API-key configuration

---

## How It Works

CyberTools Log Analyzer processes authentication logs and extracts security-relevant information.

```text
Authentication Log
        |
        v
    Log Parsing
        |
        v
   Event Extraction
        |
        v
IP / Username Analysis
        |
        v
   Risk Analysis
        |
        v
AbuseIPDB Enrichment
        |
        v
   PDF + TXT Reports
```

---

## Requirements

Before installing CyberTools Log Analyzer, make sure you have:

- Python 3
- Git
- Internet connection for AbuseIPDB enrichment
- An AbuseIPDB API key if IP reputation enrichment is required

The core log-analysis functionality can be used without an AbuseIPDB API key, but AbuseIPDB-based IP enrichment will not be available.

---

# Installation

## Windows

### 1. Install Git

Verify Git:

```powershell
git --version
```

### 2. Install Python

Verify Python:

```powershell
python --version
```

A Python 3 version should be displayed.

### 3. Clone the Repository

```powershell
git clone https://github.com/altafreza345-gif/cybertools-log-analyzer.git
```

Enter the project directory:

```powershell
cd cybertools-log-analyzer
```

### 4. Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Your terminal should show:

```text
(.venv)
```

### 5. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

### 6. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 7. Verify Installation

```powershell
python --version
pip --version
```

---

# Kali Linux

CyberTools Log Analyzer can also be used on Kali Linux.

### 1. Verify Python and Git

```bash
python3 --version
```

```bash
git --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/altafreza345-gif/cybertools-log-analyzer.git
```

Enter the project directory:

```bash
cd cybertools-log-analyzer
```

### 3. Create a Virtual Environment

```bash
python3 -m venv .venv
```

If Kali reports that the virtual-environment package is missing:

```bash
sudo apt update
sudo apt install python3-venv
```

Then create the environment:

```bash
python3 -m venv .venv
```

### 4. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

Your terminal should show:

```text
(.venv)
```

### 5. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 6. Install Dependencies

```bash
pip install -r requirements.txt
```

### 7. Verify Installation

```bash
python --version
pip --version
```

---

# AbuseIPDB API Configuration

CyberTools Log Analyzer can use AbuseIPDB for IP reputation and abuse information.

Each user should use their own AbuseIPDB API key.

## 1. Create an AbuseIPDB API Key

Create an AbuseIPDB account and generate an API key from your account.

## 2. Create Your Local `.env` File

The repository contains:

```text
.env.example
```

Copy it to:

```text
.env
```

### Windows

```powershell
Copy-Item .env.example .env
```

### Kali Linux

```bash
cp .env.example .env
```

## 3. Add Your API Key

Open `.env` using your preferred editor.

For example:

```bash
nano .env
```

Add:

```env
ABUSEIPDB_API_KEY=YOUR_ACTUAL_API_KEY
```

Replace `YOUR_ACTUAL_API_KEY` with your own API key.

Save the file.

---

# Running CyberTools Log Analyzer

Activate your virtual environment first.

### Windows

```powershell
.venv\Scripts\Activate.ps1
```

### Kali Linux

```bash
source .venv/bin/activate
```

Then run:

```bash
python loganalyzer.py
```

Follow the prompts provided by the application.

---

# Input Logs

CyberTools Log Analyzer is designed for authentication and security log analysis.

The analyzer can process authentication logs containing security-relevant events such as failed authentication activity and SSH authentication events supported by the current parser.

For testing, use authorized sample/test logs.

Do not publish private production logs to the repository.

---

# Generated Reports

Generated reports are stored in:

```text
reports/
```

The analyzer can generate:

```text
PDF report
TXT report
```

The PDF report includes CyberTools branding and structured security-analysis information.

Report information can include:

- Analysis summary
- Failed authentication activity
- Source IP information
- Attempt counts
- Targeted usernames
- First-seen timestamp
- Last-seen timestamp
- Activity duration
- Risk score
- Risk classification
- IP intelligence information
- AbuseIPDB enrichment when configured

---

# Project Structure

```text
cybertools-log-analyzer/
│
├── assets/
│   └── cybertools_logo.png
│
├── reports/
│   └── generated reports
│
├── .env.example
├── .gitignore
├── loganalyzer.py
├── requirements.txt
├── README.md
└── LICENSE
```

### Important Files

| File | Purpose |
|------|---------|
| `loganalyzer.py` | Main Log Analyzer application |
| `.env.example` | API-key configuration template |
| `.gitignore` | Prevents sensitive/local files from being committed |
| `requirements.txt` | Python dependencies |
| `assets/cybertools_logo.png` | CyberTools report branding |
| `reports/` | Generated reports |

---

# Troubleshooting

## Python command not found

Check:

```bash
python --version
```

On Kali Linux:

```bash
python3 --version
```

Make sure Python is installed and available in your PATH.

---

## Virtual Environment Does Not Activate

### Windows

```powershell
.venv\Scripts\Activate.ps1
```

### Kali Linux

```bash
source .venv/bin/activate
```

---

## Dependencies Are Missing

Run:

```bash
pip install -r requirements.txt
```

If necessary:

```bash
python -m pip install --upgrade pip
```

---

## AbuseIPDB Is Not Working

Check that `.env` exists in the project root:

```text
cybertools-log-analyzer/
├── .env
├── loganalyzer.py
└── ...
```

Check that it contains:

```env
ABUSEIPDB_API_KEY=YOUR_ACTUAL_API_KEY
```

Make sure the API key is valid.

---

## AbuseIPDB API Key Is Missing

The local log-analysis functionality can still operate without an AbuseIPDB API key, but AbuseIPDB-based IP enrichment will not be available.

---

## CyberTools Logo Is Missing From Reports

Make sure the file exists at:

```text
assets/cybertools_logo.png
```

The filename must match exactly.

---

# Security and Privacy

Authentication logs may contain sensitive information such as:

- IP addresses
- usernames
- timestamps
- authentication events
- system information

Handle logs responsibly.

Do not publish private production logs, credentials, API keys, or other sensitive information.

When AbuseIPDB enrichment is enabled, relevant IP information may be sent to the external AbuseIPDB service according to its API/service behavior.

Users should review the applicable AbuseIPDB terms and privacy policies before using the integration with sensitive data.

---

# Responsible Use

Use CyberTools Log Analyzer only on systems, logs, and data that you are authorized to analyze.

Do not use the tool to access, monitor, or investigate systems without appropriate authorization.

The developers are not responsible for misuse of the software.

---

# License

CyberTools Log Analyzer is released under the MIT License.

See the `LICENSE` file for the complete license text.

The MIT License permits use, modification, distribution, and other uses subject to the terms of the license.

---

# CyberTools Branding

The source code is distributed under the MIT License.

The CyberTools name, logo, and official branding identify the original CyberTools project.

Modified or redistributed versions should clearly identify their modifications and should not falsely represent themselves as official CyberTools releases.

---

# Roadmap

Planned improvements include:

- More SSH authentication-event detection
- Successful login analysis
- Invalid-user detection
- SSH identification-string event analysis
- Authentication-event correlation
- Improved brute-force pattern detection
- More advanced IP behavior analysis
- Additional log formats
- Expanded security intelligence integrations
- More detailed report analytics
- Additional CyberTools security-analysis modules

Roadmap items are planned improvements and may not be implemented in the current release.

---

# Contributing

Contributions, suggestions, bug reports, and improvements are welcome.

Before submitting changes:

1. Test the application.
2. Do not include API keys.
3. Do not include private logs.
4. Do not commit generated reports containing sensitive information.
5. Keep changes focused and documented.

---

# Disclaimer

CyberTools Log Analyzer is provided for defensive security analysis, education, authorized investigations, and legitimate security operations.

Always obtain appropriate authorization before analyzing systems or data that you do not own or administer.