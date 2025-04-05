import os
import faiss
import numpy as np
from openai import OpenAI
from typing import List, Tuple
from uuid import uuid4

openai_client = OpenAI()  # vai usar a OPENAI_API_KEY no ambiente

# Ajustes básicos de chunk
CHUNK_SIZE = 500  # tokens ou caracteres
CHUNK_OVERLAP = 50

def dividir_em_chunks(texto: str) -> List[str]:
    chunks = []
    i = 0
    while i < len(texto):
        chunk = texto[i:i + CHUNK_SIZE]
        chunks.append(chunk)
        i += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def gerar_embedding(texto: str) -> List[float]:
    response = openai_client.embeddings.create(
        input=texto,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def indexar_chunks(chunks: List[str]) -> Tuple[faiss.IndexFlatL2, List[str]]:
    embeddings = [gerar_embedding(chunk) for chunk in chunks]
    vetor_np = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(vetor_np)

    return index, chunks

def buscar_similares(pergunta: str, index: faiss.IndexFlatL2, chunks: List[str], top_k: int = 3) -> List[str]:
    pergunta_emb = gerar_embedding(pergunta)
    pergunta_np = np.array([pergunta_emb]).astype("float32")

    distancias, indices = index.search(pergunta_np, top_k)
    resultados = [chunks[i] for i in indices[0]]
    return resultados
