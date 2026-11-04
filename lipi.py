
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lipi Studio</title>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #1e1e1e;
    color: #ccc;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

header {
    height: 42px;
    background: #181818;
    border-bottom: 1px solid #333;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 15px;
}

.logo {
    color: #42a5ff;
    font-size: 19px;
    font-weight: bold;
}

.workspace {
    display: flex;
    height: calc(100vh - 66px);
}

.sidebar {
    width: 190px;
    background: #181818;
    border-right: 1px solid #333;
    padding: 15px 10px;
}

.sidebar h3 {
    font-size: 11px;
    color: #999;
    font-weight: normal;
}

.file {
    padding: 9px;
    background: #252526;
    font-size: 13px;
    color: #ddd;
}

.file::before {
    content: "◇ ";
    color: #42a5ff;
}

.main {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
}

.tab {
    height: 38px;
    background: #181818;
    padding: 12px;
    font-size: 13px;
    border-bottom: 1px solid #333;
}

.tab span {
    color: #42a5ff;
}

.toolbar {
    height: 42px;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 12px;
    border-bottom: 1px solid #333;
}

.toolbar button {
    border: none;
    border-radius: 0;
    padding: 7px 13px;
    color: white;
    cursor: pointer;
}

.run {
    background: #16834b;
}

.download {
    background: #333;
}

.editor-area {
    display: flex;
    flex: 1;
    min-height: 0;
}

#numeros {
    width: 43px;
    padding: 15px 8px;
    text-align: right;
    color: #858585;
    font: 14px/1.7 Consolas, monospace;
    white-space: pre;
    overflow: hidden;
    user-select: none;
}

textarea {
    flex: 1;
    min-width: 0;
    resize: none;
    border: none;
    outline: none;
    background: transparent;
    color: #9cdcfe;
    padding: 15px 10px;
    font: 14px/1.7 Consolas, monospace;
    tab-size: 4;
    white-space: pre;
}

.terminal {
    height: 90px;
    background: #181818;
    border-top: 1px solid #333;
    padding: 10px;
    font: 12px Consolas, monospace;
    overflow: auto;
}

.terminal-title {
    color: #aaa;
    margin-bottom: 10px;
}

#mensagem {
    color: #65d99b;
}

.preview {
    width: 40%;
    min-width: 200px;
    background: #181818;
    border-left: 1px solid #333;
    display: flex;
    flex-direction: column;
}

.preview-title {
    padding: 13px;
    font-size: 12px;
    color: #aaa;
    border-bottom: 1px solid #333;
}

#resultado {
    flex: 1;
    margin: 10px;
    background: white;
    overflow: auto;
}

.bottom {
    height: 24px;
    background: #007acc;
    display: flex;
    justify-content: space-between;
    padding: 5px 12px;
    color: white;
    font-size: 11px;
}

@media(max-width: 750px) {
    .sidebar {
        display: none;
    }
}

@media(max-width: 550px) {
    .workspace {
        flex-direction: column;
    }

    .main {
        min-height: 60%;
    }

    .preview {
        width: 100%;
        min-height: 35%;
    }
}
</style>
</head>

<body>

<header>
    <div class="logo">Lipi Studio</div>
    <span>Editor de programação</span>
</header>

<div class="workspace">

    <aside class="sidebar">
        <h3>EXPLORADOR</h3>
        <div class="file">editor.lp</div>
    </aside>

    <section class="main">

        <div class="tab">
            <span>◇</span> editor.lp
        </div>

        <div class="toolbar">
            <button class="run" id="executar">▶ Executar</button>
            <button class="download" id="baixar">↓ Baixar .lp</button>
        </div>

        <div class="editor-area">
            <div id="numeros">1</div>

            <textarea id="codigo" spellcheck="false">site "Meu primeiro site"

fundo "#ffffff"
cor_texto "#222222"

titulo "Bem-vindo à Lipi!"
texto "Minha primeira página."

caixa
titulo "Meu conteúdo"
texto "Criado com minha própria linguagem."
fim_caixa

botao "Clique aqui"
arredondar 0px
borda "1px solid black"
preenchimento 12px

ao clicar:
    mostrar "A Lipi está funcionando!"
fim</textarea>
        </div>

        <div class="terminal">
            <div class="terminal-title">TERMINAL</div>
            <div id="mensagem">Lipi Studio iniciado.</div>
        </div>

    </section>

    <section class="preview">
        <div class="preview-title">PRÉ-VISUALIZAÇÃO</div>
        <div id="resultado"></div>
    </section>

</div>

<div class="bottom">
    <span>Lipi Studio</span>
    <span>UTF-8 | .lp</span>
</div>

<script>
const codigo = document.getElementById("codigo");
const resultado = document.getElementById("resultado");
const mensagem = document.getElementById("mensagem");
const numeros = document.getElementById("numeros");

const area = resultado.attachShadow({mode: "open"});

const reset = document.createElement("style");

reset.textContent = `
    :host {
        display: block;
        min-height: 100%;
        color: black;
        background: white;
    }

    button {
        all: unset;
        display: inline-block;
        cursor: pointer;
    }
`;

area.appendChild(reset);

const pagina = document.createElement("div");
area.appendChild(pagina);

function atualizarNumeros() {
    const quantidade = codigo.value.split("\n").length;

    numeros.textContent = Array.from(
        {length: quantidade},
        (_, i) => i + 1
    ).join("\n");
}

codigo.addEventListener("input", atualizarNumeros);

codigo.addEventListener("scroll", () => {
    numeros.scrollTop = codigo.scrollTop;
});

codigo.addEventListener("keydown", function(event) {
    if (event.key === "Tab") {
        event.preventDefault();

        const inicio = this.selectionStart;
        const fim = this.selectionEnd;

        this.value =
            this.value.substring(0, inicio) +
            "    " +
            this.value.substring(fim);

        this.selectionStart = this.selectionEnd = inicio + 4;

        atualizarNumeros();
    }
});

function pegarTexto(linha, comando) {
    return linha.slice(comando.length).trim()
        .replace(/^["']|["']$/g, "");
}

function argumentos(linha) {
    return [...linha.matchAll(/"([^"]*)"|'([^']*)'/g)]
        .map(item => item[1] ?? item[2]);
}

function valorCSS(valor, propriedade) {
    if (/^-?\d+(\.\d+)?$/.test(valor)) {
        valor += "px";
    }

    if (!CSS.supports(propriedade, valor)) {
        throw new Error("Valor CSS inválido: " + valor);
    }

    return valor;
}

function estilo(elemento, propriedade, valor) {
    elemento.style[propriedade] = valor;
}

function executar() {
    pagina.replaceChildren();
    pagina.removeAttribute("style");

    let ultimoElemento = null;
    let ultimoBotao = null;
    let pilha = [pagina];

    const linhas = codigo.value.split("\n");

    function adicionar(elemento) {
        pilha[pilha.length - 1].appendChild(elemento);
        ultimoElemento = elemento;
        return elemento;
    }

    function criar(tag, texto) {
        const elemento = document.createElement(tag);
        elemento.textContent = texto;
        return adicionar(elemento);
    }

    function alvo() {
        return ultimoElemento || pagina;
    }

    function numero(linha, comando, maximo) {
        const valor = Number(pegarTexto(linha, comando));

        if (!Number.isFinite(valor) ||
            valor < 0 ||
            valor > maximo) {
            throw new Error("Número inválido em " + comando);
        }

        return valor;
    }

    try {

        for (let i = 0; i < linhas.length; i++) {

            const linha = linhas[i].trim();

            if (!linha || linha.startsWith("#")) continue;

            if (linha.startsWith("site ")) {
                document.title = "Lipi — " + pegarTexto(linha, "site");
            }

            else if (linha.startsWith("fundo ")) {
                const cor = pegarTexto(linha, "fundo");

                if (!CSS.supports("color", cor)) {
                    throw new Error("Cor inválida em fundo.");
                }

                pagina.style.background = cor;
            }

            else if (linha.startsWith("cor_texto ")) {
                const cor = pegarTexto(linha, "cor_texto");

                if (!CSS.supports("color", cor)) {
                    throw new Error("Cor de texto inválida.");
                }

                pagina.style.color = cor;
            }

            else if (linha.startsWith("titulo ")) {
                criar("h1", pegarTexto(linha, "titulo"));
            }

            else if (linha.startsWith("subtitulo ")) {
                criar("h2", pegarTexto(linha, "subtitulo"));
            }

            else if (linha.startsWith("texto ")) {
                criar("p", pegarTexto(linha, "texto"));
            }

            else if (linha.startsWith("botao ")) {
                ultimoBotao = criar("button", pegarTexto(linha, "botao"));
                ultimoBotao.type = "button";
            }

            else if (linha.startsWith("link ")) {
                const args = argumentos(linha);

                if (args.length < 2) {
                    throw new Error('Use: link "Texto" "https://..."');
                }

                const link = document.createElement("a");
                link.textContent = args[0];

                const url = new URL(args[1]);

                if (url.protocol !== "https:") {
                    throw new Error("O link precisa usar HTTPS.");
                }

                link.href = url.href;
                link.target = "_blank";
                link.rel = "noopener noreferrer";

                adicionar(link);
            }

            else if (linha.startsWith("imagem ")) {
                const url = pegarTexto(linha, "imagem");
                const endereco = new URL(url);

                if (endereco.protocol !== "https:") {
                    throw new Error("A imagem precisa usar HTTPS.");
                }

                const img = document.createElement("img");
                img.src = endereco.href;
                img.alt = "Imagem Lipi";

                adicionar(img);
            }

            else if (linha.startsWith("campo ")) {
                const input = document.createElement("input");
                input.placeholder = pegarTexto(linha, "campo");
                adicionar(input);
            }

            else if (linha === "caixa" ||
                     linha === "linha" ||
                     linha === "coluna") {

                const div = document.createElement("div");

                if (linha === "linha" || linha === "coluna") {
                    div.style.display = "flex";
                    div.style.flexDirection =
                        linha === "linha" ? "row" : "column";
                }

                adicionar(div);
                pilha.push(div);
            }

            else if (linha === "fim_caixa" ||
                     linha === "fim_linha" ||
                     linha === "fim_coluna") {

                if (pilha.length === 1) {
                    throw new Error("Não existe uma caixa aberta.");
                }

                pilha.pop();
                ultimoElemento = pilha[pilha.length - 1];
            }

            else if (linha === "separador") {
                criar("hr", "");
            }

            else if (linha === "quebra") {
                adicionar(document.createElement("br"));
            }

            else if (linha.startsWith("fundo_elemento ")) {
                const cor = pegarTexto(linha, "fundo_elemento");

                if (!CSS.supports("color", cor)) {
                    throw new Error("Cor inválida.");
                }

                estilo(alvo(), "backgroundColor", cor);
            }

            else if (linha.startsWith("cor_fundo_elemento ")) {
                const cor = pegarTexto(linha, "cor_fundo_elemento");

                if (!CSS.supports("color", cor)) {
                    throw new Error("Cor inválida.");
                }

                estilo(alvo(), "backgroundColor", cor);
            }

            else if (linha.startsWith("cor_texto_elemento ")) {
                const cor = pegarTexto(linha, "cor_texto_elemento");

                if (!CSS.supports("color", cor)) {
                    throw new Error("Cor inválida.");
                }

                estilo(alvo(), "color", cor);
            }

            else if (linha.startsWith("largura ")) {
                estilo(alvo(), "width",
                    valorCSS(pegarTexto(linha, "largura"), "width"));
            }

            else if (linha.startsWith("altura ")) {
                estilo(alvo(), "height",
                    valorCSS(pegarTexto(linha, "altura"), "height"));
            }

            else if (linha.startsWith("margem ")) {
                estilo(alvo(), "margin",
                    valorCSS(pegarTexto(linha, "margem"), "margin"));
            }

            else if (linha.startsWith("preenchimento ")) {
                estilo(alvo(), "padding",
                    valorCSS(pegarTexto(linha, "preenchimento"), "padding"));
            }

            else if (linha.startsWith("arredondar ")) {
                estilo(alvo(), "borderRadius",
                    valorCSS(pegarTexto(linha, "arredondar"), "borderRadius"));
            }

            else if (linha.startsWith("borda ")) {
                const valor = pegarTexto(linha, "borda");

                if (!CSS.supports("border", valor)) {
                    throw new Error("Borda inválida.");
                }

                estilo(alvo(), "border", valor);
            }

            else if (linha.startsWith("sombra ")) {
                const valor = pegarTexto(linha, "sombra");

                if (!CSS.supports("box-shadow", valor)) {
                    throw new Error("Sombra inválida.");
                }

                estilo(alvo(), "boxShadow", valor);
            }

            else if (linha.startsWith("tamanho ")) {
                estilo(alvo(), "fontSize",
                    valorCSS(pegarTexto(linha, "tamanho"), "fontSize"));
            }

            else if (linha.startsWith("fonte ")) {
                const valor = pegarTexto(linha, "fonte");

                if (!CSS.supports("font-family", valor)) {
                    throw new Error("Fonte inválida.");
                }

                estilo(alvo(), "fontFamily", valor);
            }

            else if (linha === "negrito") {
                estilo(alvo(), "fontWeight", "bold");
            }

            else if (linha.startsWith("alinhar ")) {
                const valor = pegarTexto(linha, "alinhar");
                const opcoes = {
                    centro: "center",
                    esquerda: "left",
                    direita: "right",
                    justificar: "justify"
                };

                if (!opcoes[valor]) {
                    throw new Error("Alinhamento inválido.");
                }

                estilo(alvo(), "textAlign", opcoes[valor]);
            }

            else if (linha.startsWith("opacidade ")) {
                const valor = numero(linha, "opacidade", 1);
                estilo(alvo(), "opacity", valor);
            }

            else if (linha.startsWith("display ")) {
                const valor = pegarTexto(linha, "display");

                if (!CSS.supports("display", valor)) {
                    throw new Error("Display inválido.");
                }

                estilo(alvo(), "display", valor);
            }

            else if (linha.startsWith("direcao ")) {
                const valor = pegarTexto(linha, "direcao");
                const opcoes = {
                    linha: "row",
                    coluna: "column"
                };

                if (!opcoes[valor]) {
                    throw new Error("Use linha ou coluna.");
                }

                estilo(alvo(), "flexDirection", opcoes[valor]);
            }

            else if (linha.startsWith("gap ")) {
                estilo(alvo(), "gap",
                    valorCSS(pegarTexto(linha, "gap"), "gap"));
            }

            else if (linha.startsWith("espacamento ")) {
                estilo(alvo(), "marginBottom",
                    valorCSS(pegarTexto(linha, "espacamento"), "marginBottom"));
            }

            else if (linha === "animacao crescer") {
                const elemento = alvo();

                elemento.style.transition = "transform .2s";

                elemento.addEventListener("mouseenter", () => {
                    elemento.style.transform = "scale(1.08)";
                });

                elemento.addEventListener("mouseleave", () => {
                    elemento.style.transform = "scale(1)";
                });
            }

            else if (linha === "animacao brilhar") {
                estilo(alvo(), "boxShadow", "0 0 15px #168cff");
            }

            else if (linha === "ao clicar:") {

                if (!ultimoElemento) {
                    throw new Error("Crie um elemento antes de ao clicar.");
                }

                const elemento = ultimoElemento;
                const acoes = [];
                let encontrouFim = false;

                for (let j = i + 1; j < linhas.length; j++) {
                    const interna = linhas[j].trim();

                    if (interna === "fim") {
                        encontrouFim = true;
                        i = j;
                        break;
                    }

                    if (interna.startsWith("mostrar ")) {
                        acoes.push({
                            tipo: "mostrar",
                            valor: pegarTexto(interna, "mostrar")
                        });
                    }

                    else if (interna.startsWith("mudar_texto ")) {
                        acoes.push({
                            tipo: "texto",
                            valor: pegarTexto(interna, "mudar_texto")
                        });
                    }

                    else if (interna.startsWith("mudar_fundo ")) {
                        acoes.push({
                            tipo: "fundo",
                            valor: pegarTexto(interna, "mudar_fundo")
                        });
                    }

                    else if (interna !== "") {
                        throw new Error("Ação desconhecida: " + interna);
                    }
                }

                if (!encontrouFim) {
                    throw new Error("Está faltando o comando fim.");
                }

                elemento.addEventListener("click", () => {
                    for (const acao of acoes) {
                        if (acao.tipo === "mostrar") {
                            alert(acao.valor);
                        }

                        if (acao.tipo === "texto") {
                            elemento.textContent = acao.valor;
                        }

                        if (acao.tipo === "fundo") {
                            if (!CSS.supports("color", acao.valor)) {
                                alert("Cor inválida.");
                                continue;
                            }

                            pagina.style.background = acao.valor;
                        }
                    }
                });
            }

            else {
                throw new Error("Comando desconhecido: " + linha);
            }
        }

        if (pilha.length !== 1) {
            throw new Error("Você esqueceu de fechar uma caixa.");
        }

        mensagem.textContent = "> Lipi executada com sucesso!";
        mensagem.style.color = "#65d99b";

    } catch (erro) {
        pagina.replaceChildren();

        mensagem.textContent = "> ERRO: " + erro.message;
        mensagem.style.color = "#ff6868";
    }
}

function baixar() {
    const arquivo = new Blob(
        [codigo.value],
        {type: "text/plain;charset=utf-8"}
    );

    const url = URL.createObjectURL(arquivo);
    const link = document.createElement("a");

    link.href = url;
    link.download = "meu-projeto.lp";
    link.click();

    setTimeout(() => URL.revokeObjectURL(url), 1000);
}

document.getElementById("executar").addEventListener("click", executar);
document.getElementById("baixar").addEventListener("click", baixar);

atualizarNumeros();
executar();
</script>

</body>
</html>
