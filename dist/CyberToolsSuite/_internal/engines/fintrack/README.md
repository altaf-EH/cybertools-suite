# FinTrack

**Financial Fraud & Mule Account Link Analyzer**

FinTrack is a Python-based tool for analyzing financial transaction data, account relationships, risk indicators, and generating investigation reports.

> ⚠️ **Disclaimer:** FinTrack is an analytical/support tool. Its results are not proof that a person or account is involved in fraud or any other wrongdoing. Findings must be independently reviewed and verified by qualified authorities/investigators. The developer is not responsible for decisions, actions, losses, or consequences resulting from the use or interpretation of this tool.

## Features

* Transaction analysis
* Account profiling
* Risk indicators
* Account relationship/network analysis
* Data-quality checks
* Investigation findings
* PDF report generation

## Requirements

* Python 3.11+
* Git
* Windows / Linux / Kali Linux
* VS Code (optional)

## Installation

```bash
git clone https://github.com/altafreza345-gif/cybertools-fintrack.git
cd cybertools-fintrack
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Kali Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Example:

```bash
python main.py --input input/sample_transactions.csv --output reports --case-id CASE-001
```

Generated reports and analysis artifacts will be stored in the specified output directory.

## VS Code

Open the project folder in VS Code:

```bash
code .
```

Then open the VS Code terminal, activate the virtual environment, install requirements, and run the command above.

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)** License. 

- **Personal & Internal Use Only**: You are free to run and use this tool.
- **No Commercial Use**: Commercial exploitation, selling, or renting this software is strictly prohibited.
- **No Modifications**: You cannot redistribute modified versions of this code under another name.
- **No Liability**: The software is provided "as is" without any warranties.

For more details, see the full [LICENSE](LICENSE) file.

**CyberTools / FinTrack — Active Development**
