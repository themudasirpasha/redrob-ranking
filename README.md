# 🏆 Redrob Hackathon — Intelligent Candidate Discovery & Ranking
### Submission by Team Perfect Matchmakers
#### Hack2Skill × Redrob AI | India Runs Hackathon

---

## 🎯 Problem Statement
Recruiters go through hundreds of profiles and still miss the right person — not because talent isn't there, but because keyword filters can't see what actually matters.

We built an AI system that ranks candidates the way a great recruiter would — not by matching keywords, but by actually understanding who fits the role.

---

## 🧠 Our Approach
Hybrid scoring system that ranks 1,00,000 candidates for a Senior AI Engineer role at Redrob AI using semantic understanding + behavioral signals + career depth analysis.

### What makes our system different:
- **We read intent, not keywords** — "built a retrieval pipeline" scores as high as "FAISS" in skills
- **Career history over skill lists** — what you shipped matters more than what you listed
- **Behavioral signals** — a perfect-on-paper candidate who hasn't logged in for 6 months is not actually available
- **Honeypot detection** — fake/trap profiles removed before scoring

---

## 📊 Scoring Formula
Final Score = 0.35 × Semantic + 0.25 × Skills + 0.22 × Career Depth + 0.10 × Experience + 0.08 × Availability

| Component | Weight | What it measures |
|-----------|--------|-----------------|
| Semantic Match | 35% | BGE embeddings cosine similarity — JD vs candidate |
| Skills Score | 25% | 30 must-have skills + endorsement weighting + assessment scores |
| Career Depth | 22% | Production keywords, AI/ML tenure, job hopper penalty, researcher penalty |
| Experience | 10% | Years in band, location, education tier |
| Availability | 8% | 23 behavioral signals — active date, response rate, notice period |

---

## 🔍 Filters Applied
- India only
- Experience: 4–15 years
- Open to work: True
- Notice period: ≤ 90 days
- Title whitelist: ML Engineer, AI Engineer, Data Scientist, NLP Engineer etc.
- Consulting-only careers: Removed
- Honeypot profiles: Removed at filter stage
- Result: 1,00,000 → 214 high-quality candidates → Top 100

---

## 🛠️ Tech Stack
- Python 3.11
- BAAI/bge-base-en-v1.5 (sentence-transformers)
- scikit-learn (cosine similarity)
- pandas, numpy, python-docx

---
## System Architecture

 <img width="1363" height="621" alt="image" src="https://github.com/user-attachments/assets/67c86a77-2ce4-42a3-a9db-af9b3df319da" />


## ▶️ How to Run
```bash
pip install -r requirements.txt
python rank.py --candidates ./candidates.jsonl --out ./submission.csv
```

---

## 🔗 Sandbox
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1kcVc_I6MsyNHmsGbIfKBXEfafoG_HhtZ?usp=sharing)

---

## 👥 Team Perfect Matchmakers
- Mudasir Pasha
- Voni Purujit

---

*Submitted for Redrob AI Intelligent Candidate Discovery & Ranking Challenge on Hack2Skill*
