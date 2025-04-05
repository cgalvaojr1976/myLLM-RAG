
let contextosDisponiveis = [];

function mostrar(id) {
    document.querySelectorAll('.aba').forEach(sec => sec.style.display = 'none');
    document.getElementById(id).style.display = 'block';
}

async function uploadPDFs() {
    const files = document.getElementById('pdfs').files;
    for (let file of files) {
        const formData = new FormData();
        formData.append("file", file);
        await fetch("http://localhost:8000/upload_pdf/", {
            method: "POST",
            body: formData
        });
    }
    alert("Upload concluído!");
}

async function indexarContexto() {
    const contexto = document.getElementById('contexto').value;
    const files = document.getElementById('pdfs').files;
    const nomes = Array.from(files).map(f => f.name);
    if (!contexto || nomes.length === 0) return alert("Complete os campos!");

    document.getElementById('loading').classList.remove("oculto");

    await fetch("http://localhost:8000/indexar_varios/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome_contexto: contexto, arquivos: nomes })
    });

    document.getElementById('loading').classList.add("oculto");

    if (!contextosDisponiveis.includes(contexto)) {
        contextosDisponiveis.push(contexto);
        atualizarDropdownContextos();
    }

    alert("Indexação concluída!");
}

function atualizarDropdownContextos() {
    const select = document.getElementById('contexto_pergunta');
    select.innerHTML = "";
    contextosDisponiveis.forEach(ctx => {
        const option = document.createElement("option");
        option.value = ctx;
        option.textContent = ctx;
        select.appendChild(option);
    });
}

async function consultar() {
    const contexto = document.getElementById('contexto_pergunta').value;
    const pergunta = document.getElementById('pergunta').value;
    const modelo = document.getElementById('modelo').value;

    const resp = await fetch("http://localhost:8000/perguntar/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome_contexto: contexto, pergunta, modelo })
    });
    const data = await resp.json();

    document.getElementById("resposta_rag").innerHTML = "<strong>Com RAG:</strong><br>" + (data.resposta_com_rag || "Erro");
    document.getElementById("resposta_pura").innerHTML = "<strong>Sem RAG:</strong><br>" + (data.resposta_sem_rag || "Erro");
}
