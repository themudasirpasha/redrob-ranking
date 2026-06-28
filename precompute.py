import json
import numpy as np
from sentence_transformers import SentenceTransformer
from datetime import datetime, date

# Load candidates
print("Loading candidates...")
candidates = []
with open('candidates.jsonl', 'r') as f:
    for line in f:
        if line.strip():
            candidates.append(json.loads(line))
print(f"Loaded: {len(candidates)}")

# Filter candidates
consulting = ['tcs', 'infosys', 'wipro', 'accenture', 'cognizant', 'capgemini']
filtered = []
for c in candidates:
    yoe = c['profile']['years_of_experience']
    country = c['profile']['country']
    sig = c['redrob_signals']
    if not (4 <= yoe <= 12): continue
    if country != 'India': continue
    if not sig['open_to_work_flag']: continue
    if sig['notice_period_days'] > 90: continue
    all_consulting = all(any(x in job['company'].lower() for x in consulting) for job in c['career_history'])
    if all_consulting: continue
    bad_titles = ['frontend', 'project manager', 'mechanical', 'civil', 'marketing',
                  'hr ', 'content', 'sales', 'graphic', 'designer', 'accountant',
                  'finance', 'customer support', 'customer service', 'operations manager',
                  'business analyst', 'computer vision', 'data engineer',
                  'backend engineer', 'data analyst']
    title = c['profile']['current_title'].lower()
    if any(x in title for x in bad_titles): continue
    filtered.append(c)

print(f"Filtered: {len(filtered)}")

# Save filtered candidates
with open('filtered_candidates.json', 'w') as f:
    json.dump(filtered, f)

# Create embeddings
def candidate_to_text(c):
    p = c['profile']
    skills = ', '.join([f"{s['name']} ({s['proficiency']})" for s in c['skills']])
    career = ' '.join([f"{j['title']} at {j['company']} ({j['duration_months']} months)" for j in c['career_history']])
    return f"{p['current_title']} with {p['years_of_experience']} years. Location: {p['location']}, {p['country']}. Skills: {skills}. Career: {career}. {p['summary']}"

print("Loading model...")
model = SentenceTransformer('BAAI/bge-base-en-v1.5')

print("Creating embeddings...")
texts = [candidate_to_text(c) for c in filtered]
embeddings = model.encode(texts, batch_size=128, show_progress_bar=True)
np.save('embeddings.npy', embeddings)
print(f"Embeddings saved! Shape: {embeddings.shape}")
