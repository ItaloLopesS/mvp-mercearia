const form = document.getElementById("formProduto");
const lista = document.getElementById("listaProdutos");

async function atualizarLista() {
    const resposta = await fetch("/produtos");
    const produtos = await resposta.json();

    lista.innerHTML = "";

    produtos.forEach(function(produto) {
        const linha = document.createElement("tr");

        linha.innerHTML = `
            <td>${produto.nome}</td>
            <td>${produto.quantidade}</td>
            <td>R$ ${produto.preco.toFixed(2)}</td>
            <td>-</td>
        `;

        lista.appendChild(linha);
    });
}

form.addEventListener("submit", async function(event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value;
    const quantidade = Number(document.getElementById("quantidade").value);
    const preco = Number(document.getElementById("preco").value);

    if (!nome.trim() || quantidade < 0 || preco < 0) {
        alert("Preencha os campos corretamente.");
        return;
    }

    const resposta = await fetch("/produtos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nome: nome,
            quantidade: quantidade,
            preco: preco
        })
    });

    if (resposta.ok) {
        alert("Produto cadastrado com sucesso!");
        form.reset();
        atualizarLista();
    } else {
        alert("Erro ao cadastrar produto.");
    }
});

atualizarLista();
