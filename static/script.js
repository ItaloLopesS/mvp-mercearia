const form = document.getElementById("formProduto");
const lista = document.getElementById("listaProdutos");
const seletor = document.getElementById("produtoMovimentacao");

async function atualizarLista() {
    const resposta = await fetch("/produtos");
    const produtos = await resposta.json();

    lista.innerHTML = "";
    seletor.innerHTML = '<option value="">Selecione um produto</option>';

    produtos.forEach(function(produto) {
        const linha = document.createElement("tr");

        const nome = document.createElement("td");
        nome.textContent = produto.nome;

        const quantidade = document.createElement("td");
        quantidade.textContent = produto.quantidade;

        const preco = document.createElement("td");
        preco.textContent = produto.preco.toLocaleString("pt-BR", {
            style: "currency",
            currency: "BRL"
        });

        linha.append(nome, quantidade, preco);
        lista.appendChild(linha);

        const opcao = document.createElement("option");
        opcao.value = produto.id;
        opcao.textContent = produto.nome;

        seletor.appendChild(opcao);
    });
}

form.addEventListener("submit", async function(event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const quantidade = Number(document.getElementById("quantidade").value);
    const preco = Number(document.getElementById("preco").value);

    if (!nome || quantidade < 0 || preco < 0) {
        alert("Preencha os campos corretamente.");
        return;
    }

    const resposta = await fetch("/produtos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ nome, quantidade, preco })
    });

    if (resposta.ok) {
        alert("Produto cadastrado com sucesso!");
        form.reset();
        atualizarLista();
    } else {
        alert("Erro ao cadastrar produto.");
    }
});

async function movimentar(tipo) {
    const produtoId = seletor.value;
    const quantidade = Number(
        document.getElementById("quantidadeMovimentacao").value
    );

    if (!produtoId || !Number.isInteger(quantidade) || quantidade <= 0) {
        alert("Selecione um produto e informe uma quantidade válida.");
        return;
    }

    const resposta = await fetch(`/estoque/${tipo}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            produto_id: Number(produtoId),
            quantidade: quantidade
        })
    });

    const resultado = await resposta.json();

    if (resposta.ok) {
        alert(resultado.mensagem);
        document.getElementById("quantidadeMovimentacao").value = "";
        atualizarLista();
    } else {
        alert(resultado.detail || "Erro ao movimentar estoque.");
    }
}

document.getElementById("btnEntrada").addEventListener("click", function() {
    movimentar("entrada");
});

document.getElementById("btnSaida").addEventListener("click", function() {
    movimentar("saida");
});

atualizarLista();
