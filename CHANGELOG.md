# CyberTools Suite v1.1.0 — Production Ready

## 🚀 New Features
- **Report Registry System**: Har report ab central registry mein index ho jaati hai. Chahe report kahi bhi save ho (Desktop, Documents, Custom Folder), Dashboard aur Reports page mein automatically dikhegi.
- **AI Model Download**: Settings → AI Insights mein ab "Download Model" button visible hai. Users ab directly software se Ollama models download kar sakte hain.
- **Case-Wise Output**: Reports ab `cases/{case_id}/reports/` folder mein organize hoti hain. Har case ki reports alag folder mein.
- **Sidebar Scrolling**: Pehle sidebar half-screen par cut ho jaata tha, ab poora screen tak scroll ho sakta hai.

## 🔧 Major Fixes & Improvements
- **Reports Refresh**: Reports page par refresh button ab properly kaam karta hai. Saari reports update ho jaati hain.
- **Dashboard Stats**: Ab accurate report counts dikhte hain. Pehle galat numbers dikhte the.
- **File Explorer Filters**: Ab har engine sirf apne supported formats dikhaata hai:
  - CDR: `.csv`, `.xlsx`
  - FinTrack: `.csv`, `.xlsx`
  - Log Analyzer: `.log`, `.txt`
- **Unicode Errors**: Terminal aur GUI mein `✓` (checkmark) ki wajah se aane wale `UnicodeEncodeError` fix ho gaye. Ab `[+]` use ho raha hai.
- **Corrupt File Handling**: Agar user corrupt Excel file daalega toh ab clear error message aayega: *"File appears to be corrupted. Please open in Excel and Save As."*
- **Column Detection**: CDR, FinTrack, Log Analyzer teeno mein smart column detection improve ki gayi. Chahe column ka naam kuch bhi ho, tool automatically dhundh lega.
- **Logo Path Fix**: PDF reports mein logo ab har system pe sahi dikhega (hardcoded path hata kar dynamic path lagaya).
- **Output Directory Handling**: Agar user output directory nahi deta toh default `reports/` folder use hota hai. Agar deta hai toh wahi respect hota hai.
- **Case Management**: Case list mein `case.json` ki jagah actual case names dikhte hain.
- **Large File Support**: Chunk reading aur line-by-line reading se 1GB+ files handle hoti hain (hang nahi karta).
- **Error Handling**: Har engine ab user-friendly error messages deta hai. `exited with code 1` ki jagah samajh aane wala reason dikhta hai.

## 🔒 License
- Strict CyberTools License v1.0 added. Commercial use, modification, and redistribution strictly prohibited without written permission.

## 📂 Folder Structure
CyberToolsSuite/
├── cases/
│ └── {case_id}/
│ └── reports/ # Case-wise reports
├── reports/ # Default reports folder
├── config/
│ └── settings.json # User settings
└── report_registry.json # Central report index

text

## 📦 Installation
Download `CyberToolsSuite_Setup_v1.1.0.exe` and run.

## ⬆️ Update from v1.0.0
- Download the new installer
- Run it — your existing data (cases, reports, settings) will be preserved
- Launch CyberTools Suite v1.1.0

## 👨‍💻 Developer Notes
- Version: v1.1.0
- Build: 2026-08-30
- Python 3.11 + PySide6 + Pandas + ReportLab + OpenPyXL
- Offline-first, no internet dependency (except optional Ollama download)

---
**CyberTools Team (c) 2026 — All Rights Reserved**