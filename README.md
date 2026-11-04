# Lipi 0.2

Lipi é um projeto experimental de linguagem simples, em português, para gerar páginas web e cenas 3D.

## O que esta versão faz

- Lê arquivos com extensão `.lp`.
- Gera HTML/CSS para sites.
- Oferece comandos iniciais para texto, títulos, imagens, botões, cores e efeitos.
- Gera uma cena 3D básica com Three.js (requer internet no navegador).
- Inclui uma ação simples de clique com `ao clicar:` e `mostrar`.

> Esta é uma versão inicial/experimental, não uma linguagem completa. Ainda não possui editor online, física, colisões, sistema de variáveis ou jogador controlável.

## Requisitos

- Python 3.9 ou superior.
- Para abrir jogos 3D, conexão com a internet para carregar Three.js.

## Como executar

No terminal, dentro da pasta do projeto:

```bash
python lipi.py examples/site.lp
```

Isso gera `examples/site.html`. Abra esse HTML no navegador.

Para o exemplo 3D:

```bash
python lipi.py examples/jogo.lp
```

Isso gera `examples/jogo.html`.

Para escolher outro arquivo de saída:

```bash
python lipi.py examples/site.lp --saida meu-site.html
```

## Sintaxe inicial

```text
site "Nome do site"
fundo "#101020"
cor_texto "#ffffff"
titulo "Olá!"
texto "Meu primeiro site"
botao "Clique"
animacao crescer
arredondar 16
ao clicar:
    mostrar "Funcionou!"
fim
```

Comandos 3D:

```text
jogo "Meu jogo"
cenario "#87ceeb"
chao verde
cubo 0 0 0 azul
jogador
```

## Publicar no GitHub

1. Crie um repositório público chamado `lipi`.
2. Envie os arquivos e pastas deste projeto para o repositório.
3. Confira se `README.md`, `lipi.py` e `examples/` aparecem na página.
4. O repositório público já publica o código-fonte da linguagem.
5. GitHub Pages pode hospedar uma página de apresentação/documentação, mas não executa diretamente o interpretador Python.

## Licença

Projeto experimental. Escolha uma licença antes de aceitar contribuições externas.
