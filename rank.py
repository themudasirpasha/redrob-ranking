import json
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, date
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--candidates', default='candidates.jsonl')
parser.add_argument('--out', default='submission.csv')
args = parser.parse_args()

# Load filtered candidates
print("Loading candidates...")
with open('filtered_candidates.json', 'r') as f:
    filtered_candidates = json.load(f)

# Load embeddings
embeddings = np.load('embeddings.npy')

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# JD embedding
from docx import Document
doc = Document('job_description.docx')
jd_text = '\n'.join([para.text for para in doc.paragraphs])
jd_embedding = model.encode([jd_text])

# Semantic scores
semantic_scores = cosine_similarity(jd_embedding, embeddings)[0]

# Availability score
def availability_score(c):
    sig = c['redrob_signals']
    score = 0
    last_active = datetime.strptime(sig['last_active_date'], '%Y-%m-%d').date()
    days_inactive = (date.today() - last_active).days
    if days_inactive <= 30: score += 0.4
    elif days_inactive <= 90: score += 0.2
    if sig['open_to_work_flag']: score += 0.2
    score += sig['recruiter_response_rate'] * 0.2
    if sig['notice_period_days'] <= 30: score += 0.1
    elif sig['notice_period_days'] <= 60: score += 0.05
    if sig['willing_to_relocate']: score += 0.1
    return min(score, 1.0)

# Experience score
def experience_score(c):
    score = 0
    yoe = c['profile']['years_of_experience']
    if 5 <= yoe <= 9: score += 0.5
    elif 4 <= yoe <= 12: score += 0.3
    consulting = ['tcs', 'infosys', 'wipro', 'accenture', 'cognizant', 'capgemini']
    all_consulting = all(any(x in job['company'].lower() for x in consulting) for job in c['career_history'])
    if not all_consulting: score += 0.3
    good_locations = ['pune', 'noida', 'delhi', 'mumbai', 'hyderabad', 'bangalore']
    if any(loc in c['profile']['location'].lower() for loc in good_locations): score += 0.2
    return min(score, 1.0)

# Skills score
def skills_score(c):
    must_have = ['embeddings', 'faiss', 'pinecone', 'weaviate', 'qdrant', 'vector',
                 'sentence-transformers', 'python', 'ranking', 'retrieval', 'nlp',
                 'machine learning', 'deep learning', 'ndcg', 'search', 'recommendation',
                 'llm', 'transformers', 'pytorch', 'tensorflow', 'fine-tuning']
    candidate_skills = [s['name'].lower() for s in c['skills']]
    matched = sum(1 for skill in must_have if any(skill in cs for cs in candidate_skills))
    return min(matched / len(must_have), 1.0)

# Calculate scores
availability_arr = np.array([availability_score(c) for c in filtered_candidates])
experience_arr = np.array([experience_score(c) for c in filtered_candidates])
skills_arr = np.array([skills_score(c) for c in filtered_candidates])

final_scores = (
    0.40 * semantic_scores +
    0.25 * skills_arr +
    0.20 * experience_arr +
    0.15 * availability_arr
)

# Top 100
top_100_indices = np.argsort(final_scores)[::-1][:100]

# Build reasoning
def build_reasoning(c):
    p = c['profile']
    sig = c['redrob_signals']
    ai_roles = [j['title'] for j in c['career_history']
                if any(x in j['title'].lower() for x in
                       ['ml', 'ai', 'machine learning', 'nlp', 'search', 'recommendation', 'scientist', 'ranking'])]
    key_skills = [s['name'] for s in c['skills']
                  if any(x in s['name'].lower() for x in
                         ['embedding', 'vector', 'faiss', 'pinecone', 'retrieval', 'ranking',
                          'llm', 'transformer', 'search', 'nlp', 'qdrant', 'weaviate'])][:3]
    last_active = (date.today() - datetime.strptime(sig['last_active_date'], '%Y-%m-%d').date()).days
    role_str = f"AI/ML roles: {', '.join(ai_roles[:2])}" if ai_roles else "Applied ML background"
    skill_str = f"Core skills: {', '.join(key_skills)}" if key_skills else "General ML skills"
    avail_str = f"Active {last_active}d ago, {int(sig['recruiter_response_rate']*100)}% response rate, {sig['notice_period_days']}d notice"
    return f"{role_str}. {skill_str}. {avail_str}."

# Save CSV
results = []
for rank, idx in enumerate(top_100_indices, 1):
    c = filtered_candidates[idx]
    results.append({
        'candidate_id': c['candidate_id'],
        'rank': rank,
        'score': round(final_scores[idx], 4),
        'reasoning': build_reasoning(c)
    })

df = pd.DataFrame(results)
df.to_csv(args.out, index=False)
print(f"CSV saved: {args.out}")
