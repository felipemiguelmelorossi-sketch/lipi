
import re
import html
from pathlib import Path

VERSION = "0.1"

class Lipi:
    def __init__(self):
        self.output = []
        self.mode = None
        self.title = "Projeto Lipi"
        self.background = "#101020"
        self.elements = []

    def executar(self, codigo):
        self.output = []
        self.elements = []
        self.mode = None
        self.title = "Projeto Lipi"
        self.background = "#101020"

        for numero, linha in enumerate(codigo.splitlines(), 1):
            linha = linha.strip()

            if not linha or linha.startswith("#"):
                continue

            try:
                self.comando(linha)
            except Exception as erro:
                print(f"Erro na linha {numero}: {erro}")
                return False

        self.gerar()
        return True

    def comando(self, linha):
        partes = linha.split(maxsplit=1)
        nome = partes[0].lower()
        valor = partes[1].strip() if len(partes) > 1 else ""

        if nome == "site":
            self.mode = "site"
            self.title = self.limpar(valor)

        elif nome == "jogo":
            self.mode = "jogo"
            self.title = self.limpar(valor)

        elif nome == "fundo":
            self.background = self.limpar(valor)

        elif nome == "titulo":
            self.elements.append(
                f"<h1>{html.escape(self.limpar(valor))}</h1>"
            )

        elif nome == "texto":
            self.elements.append(
                f"<p>{html.escape(self.limpar(valor))}</p>"
            )

        elif nome == "botao":
            self.elements.append(
                f'<button onclick="alert(\'Olá da Lipi!\')">'
                f'{html.escape(self.limpar(valor))}</button>'
            )

        elif nome == "imagem":
            url = self.limpar(valor)
            if not url.startswith(("https://", "http://")):
                raise ValueError("URL de imagem inválida")
            self.elements.append(
                f'<img src="{html.escape(url, quote=True)}" '
                'style="max-width:100%;border-radius:12px">'
            )

        elif nome == "jogador":
            self.elements.append(
                '<div id="player"></div>'
            )

        elif nome == "cubo":
            dados = valor.split()
            if len(dados) < 4:
                raise ValueError("Use: cubo X Y Z cor")
            x, y, z = map(float, dados[:3])
            cor = dados[3]
            self.elements.append(
                f'<lipi-cube x="{x}" y="{y}" z="{z}" '
                f'color="{html.escape(cor, quote=True)}"></lipi-cube>'
            )

        elif nome == "chao":
            self.elements.append(
                f'<lipi-ground color="{html.escape(self.limpar(valor), quote=True)}"></lipi-ground>'
            )

        elif nome == "cenario":
            self.elements.append(
                f'<lipi-sky color="{html.escape(self.limpar(valor), quote=True)}"></lipi-sky>'
            )

        elif nome == "fim":
            self.gerar()

        else:
            raise ValueError(f"Comando desconhecido: {nome}")

    def limpar(self, valor):
        valor = valor.strip()
        if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in ('"', "'"):
            return valor[1:-1]
        return valor

    def gerar(self):
        if not self.mode:
            return

        if self.mode == "site":
            conteudo = "\n".join(self.elements)
            documento = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(self.title)}</title>
<style>
* {{ box-sizing: border-box; }}
body {{
    margin: 0;
    padding: 40px 20px;
    min-height: 100vh;
    background: {self.background};
    color: white;
    font-family: Arial, sans-serif;
    text-align: center;
}}
h1 {{ font-size: 42px; }}
p {{ font-size: 19px; color: #ccc; }}
button {{
    padding: 14px 25px;
    border: 0;
    border-radius: 10px;
    background: #087cff;
    color: white;
    font-size: 16px;
    cursor: pointer;
    transition: .2s;
}}
button:hover {{ transform: scale(1.06); }}
</style>
</head>
<body>
{conteudo}
</body>
</html>"""
            Path("index.html").write_text(documento, encoding="utf-8")
            print("Site criado: index.html")

        elif self.mode == "jogo":
            conteudo = "\n".join(self.elements)
            documento = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(self.title)}</title>
<style>
body {{ margin: 0; overflow: hidden; }}
canvas {{ display: block; }}
</style>
</head>
<body>
<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';

const cena = new THREE.Scene();
cena.background = new THREE.Color('#87ceeb');

const camera = new THREE.PerspectiveCamera(
  75, innerWidth / innerHeight, 0.1, 1000
);
camera.position.set(5, 5, 8);
camera.lookAt(0, 0, 0);

const render = new THREE.WebGLRenderer({{antialias:true}});
render.setSize(innerWidth, innerHeight);
document.body.appendChild(render.domElement);

cena.add(new THREE.HemisphereLight(0xffffff, 0x555555, 2));

const luz = new THREE.DirectionalLight(0xffffff, 2);
luz.position.set(5, 10, 5);
cena.add(luz);

function cubo(x,y,z,cor) {{
  const geo = new THREE.BoxGeometry(1,1,1);
  const mat = new THREE.MeshStandardMaterial({{color:cor}});
  const obj = new THREE.Mesh(geo,mat);
  obj.position.set(x,y,z);
  cena.add(obj);
}}

function chao(cor) {{
  const geo = new THREE.PlaneGeometry(100,100);
  const mat = new THREE.MeshStandardMaterial({{color:cor}});
  const obj = new THREE.Mesh(geo,mat);
  obj.rotation.x = -Math.PI/2;
  obj.position.y = -0.5;
  cena.add(obj);
}}

function ceu(cor) {{
  cena.background = new THREE.Color(cor);
}}

const comandos = document.querySelectorAll('lipi-cube, lipi-ground, lipi-sky');
comandos.forEach(el => {{
  if (el.tagName === 'LIPI-CUBE') {{
    cubo(Number(el.getAttribute('x')), Number(el.getAttribute('y')),
      Number(el.getAttribute('z')), el.getAttribute('color'));
  }}
  if (el.tagName === 'LIPI-GROUND') chao(el.getAttribute('color'));
  if (el.tagName === 'LIPI-SKY') ceu(el.getAttribute('color'));
}});

function animar() {{
  requestAnimationFrame(animar);
  render.render(cena,camera);
}}
animar();

addEventListener('resize', () => {{
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  render.setSize(innerWidth, innerHeight);
}});
</script>
</body>
</html>"""
            Path("index.html").write_text(documento, encoding="utf-8")
            print("Jogo 3D criado: index.html")


if __name__ == "__main__":
    print(f"Lipi {VERSION}")
    print("Digite o código Lipi. Digite SAIR para encerrar.")
    linhas = []

    while True:
        linha = input("Lipi > ")
        if linha.strip().upper() == "SAIR":
            break
        linhas.append(linha)

    codigo = "\n".join(linhas)
    Lipi().executar(codigo)
