# 🛡️ CyberTools Suite v1.1.0

**Production Ready — Law Enforcement / Cyber Cell Grade Investigation Platform**

---

## 📌 Overview

CyberTools Suite is an offline-first, privacy-focused digital investigation platform designed for **Law Enforcement Agencies, Cyber Cells, and Government Investigative Bodies**. It provides three powerful tools in one unified interface:

- **CDR Analyzer** — Call Detail Record analysis
- **FinTrack** — Financial fraud & mule account detection
- **Log Analyzer** — Authentication log analysis

All data stays on your machine. No internet required (except optional AI model download). No data leaves your system.

---

## 🔥 What's New in v1.1.0

- **Report Registry System** — Central index of all reports. Chahe report kahi bhi save ho, Dashboard mein dikhegi.
- **AI Model Download** — Download Ollama models directly from Settings.
- **Case-Wise Output** — Reports organized in `cases/{case_id}/reports/`.
- **Sidebar Scrolling** — Full sidebar scroll support (pehle half-screen cut ho jaata tha).
- **Better Error Handling** — User-friendly messages for corrupt files.
- **Smart Column Detection** — Chahe column ka naam kuch bhi ho, tool automatically dhundh lega.
- **Unicode Errors Fixed** — `✓` checkmark removed, `[+]` used.
- **Dashboard Stats Fixed** — Accurate report counts.

---

## 🛠️ Tools

| Tool | Purpose | Supported Formats |
|------|---------|-------------------|
| **CDR Analyzer** | Call Detail Record analysis (Telecom) | `.csv`, `.xlsx` |
| **FinTrack** | Financial fraud & mule account detection | `.csv`, `.xlsx` |
| **Log Analyzer** | Authentication log analysis (SSH, FTP, etc.) | `.log`, `.txt` |

---

## 📄 Report Formats

| Tool | Reports Generated |
|------|-------------------|
| CDR Analyzer | 📄 PDF |
| Log Analyzer | 📄 PDF |
| FinTrack | 📄 PDF + 📊 XLSX (Excel) |

---

## 💪 Key Features

- **Offline-First** — Data never leaves your machine. No cloud, no tracking.
- **Smart Column Detection** — Automatically detects column names. User doesn't need to rename columns.
- **Chunk Reading** — Handles 1GB+ files without crashing.
- **Crash-Proof** — Every error is handled gracefully. Clear user-friendly messages.
- **Report Registry** — Central index of all reports. Reports visible in Dashboard even if saved in custom folders.
- **Local AI (Ollama)** — Optional, free, offline. No API key required. Data never leaves your machine.
- **Case Management** — Create cases, add evidence, track investigations.
- **Evidence Tracking** — Add evidence files to cases.
- **Custom Output Directory** — User can choose where reports are saved.
- **Scrollable Sidebar** — Full sidebar scroll support.

---

## 📂 Folder Structure
CyberToolsSuite/
├── cases/
│ └── {case_id}/
│ └── reports/ # Case-wise reports
├── reports/ # Default reports folder
├── config/
│ └── settings.json # User settings
├── data/
│ └── known_patterns.json # Editable AI patterns
├── engines/
│ ├── cdr_analyzer/
│ ├── fintrack/
│ └── log_analyzer/
├── ui/
│ └── ... (UI components)
├── assets/
│ └── logo.png
├── LICENSE.txt
├── README.md
└── report_registry.json # Central report index

text

---

## 📦 Installation

### Option 1: Installer (Recommended)
1. Download `CyberToolsSuite_Setup_v1.1.0.exe`
2. Run the installer
3. Launch from Start Menu or Desktop

### Option 2: Portable
1. Download `CyberToolsSuite.exe`
2. Run directly

---

## 🔧 System Requirements

| Requirement | Minimum |
|-------------|---------|
| OS | Windows 10 / 11 |
| RAM | 4GB (8GB+ recommended for AI) |
| Disk Space | 500MB (5GB+ for AI models) |
| Python | Not required (standalone .exe) |

---

## 🧠 AI Insights (Optional)

AI Insights uses **Ollama** to provide local LLM analysis.

### Setup
1. Install Ollama from [https://ollama.com](https://ollama.com)
2. Launch CyberTools Suite
3. Go to **Settings → AI Insights**
4. Click **"Download Model"**
5. Wait for download to complete

### Supported Models

| Tier | Model | Size |
|------|-------|------|
| Fast | `llama3.2:3b` | ~2GB |
| Balanced | `phi3:mini` | ~2.3GB |
| Best | `llama3.1:8b` | ~4.7GB |

---

## 🔒 License

**Strict CyberTools License** — Commercial use, modification, and redistribution strictly prohibited without written permission.

See `LICENSE.txt` for full details.

---

## 👨‍💻 Developer

**CyberTools Team (c) 2026**

---

## 📞 Contact

For queries, feedback, or commercial licensing:
- Email: `[your-email]`
- GitHub Issues: `[your-repo-url]`

---

## 🙏 Acknowledgements

- PySide6 — Qt for Python
- Pandas — Data analysis
- ReportLab — PDF generation
- OpenPyXL — Excel support
- Ollama — Local LLM

---

**Built with ❤️ for Law Enforcement & Cyber Cells**