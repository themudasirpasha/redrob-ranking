# Redrob AI Candidate Ranking System
### Intelligent Candidate Discovery & Ranking Challenge

## Approach
Hybrid scoring system that ranks 1 lakh candidates for a Senior AI Engineer role using:
- **Semantic similarity** — sentence-transformers embeddings (all-MiniLM-L6-v2)
- **Skills matching** — JD-extracted must-have skills vs candidate skills
- **Experience quality** — years of experience, product company background, location
- **Behavioral signals** — availability, response rate, notice period, GitHub activity

## Scoring Formula 
Final Score = 0.40 × Semantic + 0.25 × Skills + 0.20 × Experience + 0.15 × Availability

## Setup
```bash
pip install -r requirements.txt
```

## How to Run

### Step 1 — Precompute embeddings (one time, internet required)
```bash
python precompute.py
```
This will:
- Load and filter candidates (India, 4-12 yrs, open to work, no consulting-only)
- Generate embeddings using sentence-transformers
- Save `filtered_candidates.json` and `embeddings.npy`

### Step 2 — Generate ranked CSV (offline, CPU only, <5 min)
```bash
python rank.py --candidates ./candidates.jsonl --out ./submission.csv
```

## Tech Stack
- Python 3.11
- sentence-transformers (all-MiniLM-L6-v2)
- scikit-learn (cosine similarity)
- pandas, numpy
- python-docx

## Filters Applied
- Country: India only
- Experience: 4-12 years
- Open to work: True
- Notice period: ≤ 90 days
- Removed: consulting-only, irrelevant titles (Frontend, Business Analyst, etc.)

## Team
- Mudasir Pasha
- Voni Purujit

## Data
Download the candidate dataset from the hackathon bundle:

[Download candidates.jsonl.gz](https://drive.google.com/file/d/1MfD47XvVdRKBGRAyzGOxDCEf2ve96Jjo/view?usp=sharing)

After downloading:
1. Place `candidates.jsonl` in root directory
2. Run `python precompute.py`
3. Run `python rank.py --candidates ./candidates.jsonl --out ./submission.csv`

## Sandbox / Demo
Run the notebook on Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1FDHlMmFm-MBIzgz9lJqI5P0IYN_0M63r?usp=sharing)
