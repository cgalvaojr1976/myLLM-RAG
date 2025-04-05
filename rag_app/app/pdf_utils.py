import fitz  # PyMuPDF

def extrair_texto_pdf(caminho_pdf):
    texto_total = ""
    with fitz.open(caminho_pdf) as doc:
        for pagina in doc:
            texto_total += pagina.get_text()
    return texto_total
