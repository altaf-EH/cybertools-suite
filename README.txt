# CyberTools Suite

**Professional Digital Investigation Platform**

CyberTools Suite is a powerful, offline-first digital investigation platform designed for cyber cell authorities, forensic investigators, SOC analysts, and law enforcement agencies.

---

## 📸 Screenshots

### Dashboard
![Dashboard](https://raw.githubusercontent.com/altaf-EH/cybertools-suite/main/assets/screenshots/dashboard.png)

### CDR Analyzer
![CDR Analyzer](https://raw.githubusercontent.com/altaf-EH/cybertools-suite/main/assets/screenshots/cdr_analyzer.png)

### Log Analyzer
![Log Analyzer](https://raw.githubusercontent.com/altaf-EH/cybertools-suite/main/assets/screenshots/log_analyzer.png)

### FinTrack
![FinTrack](https://raw.githubusercontent.com/altaf-EH/cybertools-suite/main/assets/screenshots/fintrack.png)

### Case Management
![Case Management](https://raw.githubusercontent.com/altaf-EH/cybertools-suite/main/assets/screenshots/case_management.png)

### Reports
![Reports](https://raw.githubusercontent.com/altaf-EH/cybertools-suite/main/assets/screenshots/reports.png)

### Settings
![Settings](https://raw.githubusercontent.com/altaf-EH/cybertools-suite/main/assets/screenshots/settings.png)

---

## 📋 Table of Contents

1. [Features](#features)
2. [Tools Included](#tools-included)
3. [System Requirements](#system-requirements)
4. [Installation](#installation)
5. [Getting Started](#getting-started)
6. [Using the Tools](#using-the-tools)
7. [AI Insights (Ollama)](#ai-insights-ollama)
8. [Case Management](#case-management)
9. [Reports](#reports)
10. [Supported File Formats](#supported-file-formats)
11. [Updates](#updates)
12. [Privacy & Security](#privacy--security)
13. [License](#license)
14. [Support](#support)

---

## ✨ Features

- **Offline-First**: All data stays on your PC. No cloud, no internet required for core functionality.
- **3 Analysis Engines**: CDR Analyzer, Log Analyzer, and FinTrack - all in one platform.
- **AI-Powered Insights**: Local AI analysis via Ollama - free, private, no API key needed.
- **Case Management**: Organize investigations into structured cases.
- **Professional Reports**: Generate PDF, TXT, XLSX, CSV, and JSON reports.
- **Auto-Updates**: Get new tools and bug fixes automatically via GitHub Releases.
- **Local AI**: AI runs entirely on your machine - no data leaves your PC.

---

## 🛠️ Tools Included

### 1. CDR Analyzer
Analyzes telecom Call Detail Records (CDR) to identify:
- Suspicious numbers and calling patterns
- Odd-hour activity (11PM - 5AM)
- Multiple IMEI swaps (SIM swapping)
- High call frequency and volume
- Tower/cell location patterns
- Contact pair link analysis

### 2. Log Analyzer
Analyzes authentication and security logs to identify:
- Failed login attempts
- Brute force attacks
- Multiple username targeting
- Suspicious IP addresses
- IP geolocation and reputation (via AbuseIPDB)
- Attack speed analysis

### 3. FinTrack
Analyzes financial transactions to identify:
- Mule account patterns
- Funnel account structures
- Same-day in-out fund movement (layering)
- Round-figure transactions (structuring)
- High pass-through ratio accounts
- Closed-loop transaction pairs
- Network risk cross-checks

---

## 💻 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Operating System | Windows 10 (64-bit) | Windows 11 (64-bit) |
| RAM | 8 GB | 16 GB |
| Disk Space | 500 MB | 1 GB |
| CPU | Dual-core | Quad-core or better |
| Internet | Not required (except AI model download) | Optional |

---

## 📥 Installation

### Option 1: Installer (Recommended for End Users)

1. Download `CyberToolsSuite_Setup_v1.0.0.exe` from GitHub Releases
2. Run the installer
3. Follow the on-screen instructions
4. Launch CyberTools Suite from Start Menu or Desktop

### Option 2: From Source (For Developers)

```bash
# Clone the repository
git clone https://github.com/altaf-EH/cybertools-suite.git
cd cybertools-suite

# Create virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# Create virtual environment (Linux/Mac)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
🚀 Getting Started
Step 1: Launch the App
Double-click CyberToolsSuite.exe or run python main.py

Step 2: Create a Case
Go to Case Management

Enter a Case ID (e.g., CASE-001)

Enter a Title and Description

Click Create Case

Step 3: Add Evidence
Select your case

Click Add Evidence

Choose your evidence file (CSV, XLSX, LOG, etc.)

Step 4: Run Analysis
Go to the appropriate tool (CDR Analyzer, Log Analyzer, or FinTrack)

Enter your Case ID

Select your Input File

Click Run Analysis

Step 5: View Reports
Reports are automatically saved to cases/<Case-ID>/reports/

View them in the Reports section

📊 Using the Tools
CDR Analyzer
Input: CSV, XLSX, XLS, TSV, TXT files with call records

Required Columns:

calling_number (or aliases like a_party, caller, from_number)

called_number (or aliases like b_party, callee, to_number)

date and time (or datetime)

Optional Columns:

duration - call duration in seconds

call_type - voice, SMS, data, etc.

tower_id - cell tower ID

imei - device IMEI

imsi - subscriber IMSI

Log Analyzer
Input: LOG, TXT, CSV, TSV files with authentication logs

Detects:

Failed password

Invalid user

authentication failure

Failed login

Login failed

Permission denied

Connection refused

FinTrack
Input: CSV, XLSX, XLS, TSV, TXT files with transaction records

Required Columns:

sender_account (or aliases like from_account, payer, debit_account)

receiver_account (or aliases like to_account, payee, beneficiary)

amount (or aliases like amt, txn_amount, value)

Optional Columns:

date and time (or datetime)

transaction_type - debit/credit, type

channel - payment mode

bank_name - bank/IFSC

remarks - narration/description

reference_id - UTR/RRN

🤖 AI Insights (Ollama)
What is Ollama?
Ollama is a free, open-source tool that runs large language models (LLMs) locally on your PC. It's completely offline - no data ever leaves your machine.

Why Use AI Insights?
Free: No API keys, no subscription, no per-request cost

Private: Your data never leaves your PC

Contextual: AI connects the dots between findings

Hybrid: Rules do the heavy lifting, AI adds reasoning

How to Set Up AI Insights
Install Ollama from https://ollama.com

Launch Ollama - it runs in the background

Open CyberTools Suite → Settings → AI Insights

Click Recheck Status - it should detect Ollama

Click Download Model - this downloads the AI model

Enable AI Insights

Available Models
Tier	Model	RAM Required	Quality
Fast	llama3.2:3b	8 GB	Good
Balanced	phi3:mini	8 GB	Good
Best	llama3.1:8b	16 GB	Best
How AI Insights Work
Run your analysis (CDR, Log, FinTrack)

Click Get AI Insights

The local AI model analyzes the findings

It connects patterns and suggests next steps

📁 Case Management
Create a Case
Case ID: Unique identifier (e.g., CASE-001)

Title: Investigation title

Description: Short summary

Case Structure
text
cases/
└── CASE-001/
    ├── case.json          # Case metadata
    ├── evidence/          # Evidence files
    ├── reports/           # Generated reports
    └── artifacts/         # Analysis artifacts
📄 Reports
Generated Reports
Tool	Formats
CDR Analyzer	PDF, TXT, XLSX
Log Analyzer	PDF, TXT
FinTrack	PDF, TXT, XLSX, CSV, JSON
Report Contents
Summary: Total records, unique entities, overall risk

Suspicious Entities: Ranked list with risk scores

Link Analysis: Top contact/transaction pairs

Analysis Reasons: Why each entity was flagged

📂 Supported File Formats
Tool	Supported Extensions
CDR Analyzer	.csv, .xlsx, .xls, .tsv, .txt
Log Analyzer	.log, .txt, .csv, .tsv
FinTrack	.csv, .xlsx, .xls, .tsv, .txt
Unsupported Files
If you upload an unsupported file (e.g., .png, .jpeg), the tool will show:

text
[ERROR] Unsupported file format: .png
Supported formats: .csv, .xlsx, .xls, .tsv, .txt
🔄 Updates
How Updates Work
CyberTools Suite checks GitHub Releases automatically

When a new version is available, a popup appears

Click Yes to download the update

Install the new version

Version History
Version	Date	Changes
v1.0.0	2026	Initial release
🔒 Privacy & Security
Data Privacy
100% Offline: All data stays on your PC

No Cloud: No data is uploaded to any server

Local AI: AI runs on your machine via Ollama

What Stays Local
Case files

Evidence files

Generated reports

Analysis results

AI analysis

Optional External Services
AbuseIPDB: Only when you add an API key (for IP reputation checks)

GitHub Updates: Only checks for new versions (no data sent)

📜 License
CyberTools Suite is licensed under Creative Commons BY-NC-ND 4.0 International.

Personal & Internal Use Only: Free to use for authorized investigations

No Commercial Use: Cannot be sold or rented

No Modifications: Cannot redistribute modified versions

No Liability: Software is provided "as is"

Copyright © 2026 CyberTools. All Rights Reserved.

📞 Support
GitHub
Repository: https://github.com/altaf-EH/cybertools-suite

Issues: Report bugs at https://github.com/altaf-EH/cybertools-suite/issues

Updates
Check for updates: CyberTools Suite → Settings → Check for Updates

🙏 Acknowledgments
Ollama: https://ollama.com - Local AI models

AbuseIPDB: https://www.abuseipdb.com - IP reputation

PySide6: Qt for Python - UI framework

ReportLab: PDF generation

Pandas: Data processing

PyInstaller: Executable packaging

Copyright © 2026 CyberTools. All Rights Reserved.