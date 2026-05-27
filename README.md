# AI-Powered Job Market Analyzer

Analyze **123,000+** LinkedIn job postings with interactive charts and a natural-language AI analyst (LangChain + Mistral via Ollama).

## Features

- Dashboard: salaries, top titles, companies, experience levels, remote vs on-site
- AI chat: ask questions about the dataset in plain English

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Arshan-1/Ai-Job-Analyzer.git
cd Ai-Job-Analyzer
```

### 2. Get the data

Download the dataset from Kaggle: [LinkedIn Job Postings](https://www.kaggle.com/datasets/arshan-1-or-similar) (search **"LinkedIn Job Postings"** on Kaggle).

Place `postings.csv` in the project folder, then run:

```bash
python analyze.py
```

This creates `cleaned_jobs.csv` (required by the app).

> **Note:** CSV files are not in this repo (they exceed GitHub’s 100 MB file limit). You must add them locally after cloning.

### 3. Install dependencies

```bash
python -m venv myenv
myenv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### 4. Run Ollama + Mistral (for AI chat)

```bash
ollama pull mistral
ollama serve
```

### 5. Start the app

```bash
streamlit run app.py
```

## Project structure

| File | Purpose |
|------|---------|
| `app.py` | Streamlit dashboard + AI chatbot |
| `analyze.py` | Cleans raw data → `cleaned_jobs.csv` |
| `requirements.txt` | Python dependencies |

## Tech stack

Python · Streamlit · Pandas · Plotly · LangChain · Ollama (Mistral)

## Author

[Arshan-1](https://github.com/Arshan-1)
