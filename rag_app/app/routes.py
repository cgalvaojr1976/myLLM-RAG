from fastapi import APIRouter, File, UploadFile
import os
from app.pdf_utils import extrair_texto_pdf
from app.rag_engine import dividir_em_chunks, indexar_chunks
import pickle
import faiss


router = APIRouter()

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.get("/status")
async def root():
    return {"message": "Servidor RAG ativo!"}

@router.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    caminho_arquivo = os.path.join(UPLOAD_FOLDER, file.filename)

    # Salvar o arquivo
    conteudo = await file.read()
    with open(caminho_arquivo, "wb") as f:
        f.write(conteudo)

    # Testa se o PDF é válido
    try:
        texto = extrair_texto_pdf(caminho_arquivo)
    except Exception as e:
        return {"erro": f"Falha ao abrir PDF: {str(e)}"}

    return {"arquivo": file.filename, "tamanho_texto": len(texto)}


INDEX_FOLDER = "data/indices"
os.makedirs(INDEX_FOLDER, exist_ok=True)

@router.post("/indexar_pdf/")
async def indexar_pdf(nome_arquivo: str):
    caminho_pdf = os.path.join(UPLOAD_FOLDER, nome_arquivo)

    if not os.path.exists(caminho_pdf):
        return {"erro": "Arquivo não encontrado."}

    texto = extrair_texto_pdf(caminho_pdf)
    chunks = dividir_em_chunks(texto)
    index, chunks_utilizados = indexar_chunks(chunks)

    # Salvar índice e chunks
    faiss.write_index(index, os.path.join(INDEX_FOLDER, f"{nome_arquivo}.index"))
    with open(os.path.join(INDEX_FOLDER, f"{nome_arquivo}.chunks.pkl"), "wb") as f:
        pickle.dump(chunks_utilizados, f)

    return {
        "mensagem": "Indexação concluída",
        "arquivo": nome_arquivo,
        "quantidade_chunks": len(chunks_utilizados)
    }


from typing import List
from pydantic import BaseModel

class RequisicaoIndexacaoTematica(BaseModel):
    nome_contexto: str
    arquivos: List[str]

@router.post("/indexar_varios/")
async def indexar_varios_pdf(requisicao: RequisicaoIndexacaoTematica):
    nome_contexto = requisicao.nome_contexto
    arquivos = requisicao.arquivos

    todos_chunks = []

    for nome_arquivo in arquivos:
        caminho_pdf = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        if not os.path.exists(caminho_pdf):
            return {"erro": f"Arquivo não encontrado: {nome_arquivo}"}
        
        texto = extrair_texto_pdf(caminho_pdf)
        chunks = dividir_em_chunks(texto)
        todos_chunks.extend(chunks)

    index, chunks_utilizados = indexar_chunks(todos_chunks)

    # Salvar com o nome do contexto
    faiss.write_index(index, os.path.join(INDEX_FOLDER, f"{nome_contexto}.index"))
    with open(os.path.join(INDEX_FOLDER, f"{nome_contexto}.chunks.pkl"), "wb") as f:
        pickle.dump(chunks_utilizados, f)

    return {
        "mensagem": f"Indexação temática '{nome_contexto}' concluída",
        "total_arquivos": len(arquivos),
        "total_chunks": len(chunks_utilizados)
    }


from app.rag_engine import buscar_similares
from app.openai_utils import responder_com_openai

class RequisicaoPergunta(BaseModel):
    nome_contexto: str
    pergunta: str
    modelo: str = "gpt-3.5-turbo"

@router.post("/perguntar/")
async def perguntar(req: RequisicaoPergunta):
    index_path = os.path.join(INDEX_FOLDER, f"{req.nome_contexto}.index")
    chunks_path = os.path.join(INDEX_FOLDER, f"{req.nome_contexto}.chunks.pkl")

    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        return {"erro": "Contexto temático não encontrado"}

    # Carrega o índice FAISS e os chunks
    index = faiss.read_index(index_path)
    with open(chunks_path, "rb") as f:
        chunks = pickle.load(f)

    trechos_relevantes = buscar_similares(req.pergunta, index, chunks, top_k=4)

    # Prompt com contexto
    contexto = "\n".join(trechos_relevantes)
    prompt_com_contexto = f"""Baseando-se apenas nos textos abaixo, responda à pergunta.
    
[Contexto]
{contexto}

[Pergunta]
{req.pergunta}
"""

    resposta_com_rag = responder_com_openai(prompt_com_contexto, req.modelo)
    resposta_sem_rag = responder_com_openai(req.pergunta, req.modelo)

    return {
        "modelo": req.modelo,
        "pergunta": req.pergunta,
        "resposta_com_rag": resposta_com_rag,
        "resposta_sem_rag": resposta_sem_rag
    }
