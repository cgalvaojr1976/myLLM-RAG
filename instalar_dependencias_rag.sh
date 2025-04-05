#!/bin/bash

echo "🔧 Instalando dependências do projeto RAG..."

# Verifica se o pip está instalado
if ! command -v pip &> /dev/null
then
    echo "❌ pip não encontrado. Por favor, instale o pip antes de continuar."
    exit 1
fi

# Atualiza o pip
pip install --upgrade pip

# Instala os pacotes necessários
pip install fastapi uvicorn openai PyMuPDF faiss-cpu python-multipart

echo "✅ Instalação concluída com sucesso!"
