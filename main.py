from fastapi import FastAPI, UploadFile
import numpy as np
from parser import extract_text
from embedder import get_embedding
from matcher import create_index, add_to_index, search
import os

app = FastAPI()

os.makedirs("data/resumes", exist_ok=True)
os.makedirs("data/jds", exist_ok=True)

resume_index = create_index()
jd_index = create_index()

resume_store = []
jd_store = []

resume_embeddings = []
jd_embeddings = []

@app.post("/upload/resume")
async def upload_resume(file: UploadFile):
    path = f"data/resumes/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    text = extract_text(path)
    if not text.strip():
        return {"error": "Empty or unreadable resume"}

    emb = get_embedding(text)

    resume_store.append(file.filename)
    resume_embeddings.append(emb)

    add_to_index(resume_index, np.array([emb]))
    return {"msg": "Resume uploaded", "resume_id": len(resume_store) - 1}

@app.post("/upload/jd")
async def upload_jd(file: UploadFile):
    path = f"data/jds/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    text = extract_text(path)
    if not text.strip():
        return {"error": "Empty or unreadable JD"}

    emb = get_embedding(text)

    jd_store.append(file.filename)
    jd_embeddings.append(emb)

    add_to_index(jd_index, np.array([emb]))
    return {"msg": "JD uploaded", "jd_id": len(jd_store) - 1}

@app.post("/match/resume")
def match_resume_to_jd(resume_id: int, top_k: int = 3):
    k = min(top_k, len(jd_store))
    query_emb = np.array([resume_embeddings[resume_id]])
    scores, ids = search(jd_index, query_emb, k)

    results = []
    seen = set()

    for idx, i in enumerate(ids):
        if i == -1:
            continue
        if scores[idx] < 0:
            continue
        if i in seen:
            continue

        seen.add(i)
        results.append({
            "jd": jd_store[i],
            "score": float(scores[idx])
        })

    return results


@app.post("/match/jd")
def match_jd_to_resume(jd_id: int, top_k: int = 3):
    k = min(top_k, len(resume_store))
    query_emb = np.array([jd_embeddings[jd_id]])
    scores, ids = search(resume_index, query_emb, k)

    results = []
    seen = set()

    for idx, i in enumerate(ids):
        if i == -1:
            continue
        if scores[idx] < 0:
            continue
        if i in seen:
            continue

        seen.add(i)
        results.append({
            "resume": resume_store[i],
            "score": float(scores[idx])
        })

    return results
