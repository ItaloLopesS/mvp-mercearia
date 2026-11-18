const form = document.getElementById("formProduto");
const lista = document.getElementById("listaProdutos");

let produtos = [];

form.addEventListener("submit", function(event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value;
    const quantidade = Number(document.getElementById("quantidade").value);
    const preco = Number(document.getElementById("preco").value);

    if (!nome.trim() || quantidade < 0 || preco < 0) {
        alert("Preencha os campos corretamente.");
        return;
    }

    const produto = {
        nome: nome,
        quantidade: quantidade,
        preco: preco
    };

    produtos.push(produto);

    atualizarLista();
    form.reset();
});

function atualizarLista() {
    lista.innerHTML = "";

    produtos.forEach(function(produto, indice) {
        const linha = document.createElement("tr");

        linha.innerHTML = `
            <td>${produto.nome}</td>
            <td>${produto.quantidade}</td>
            <td>R$ ${produto.preco.toFixed(2)}</td>
            <td>
                <button onclick="removerProduto(${indice})">
                    Remover
                </button>
            </td>
        `;

        lista.appendChild(linha);
    });
}

function removerProduto(indice) {
    produtos.splice(indice, 1);
    atualizarLista();
}
