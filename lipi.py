#!/usr/bin/env python3
"""Lipi 0.2 - interpretador inicial para sites e cenas 3D."""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path
from typing import List, Optional

VERSION = "0.2.0"


def value_of(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
        return raw[1:-1]
    return raw


def safe_color(value: str) -> str:
    value = value_of(value)
    if not re.fullmatch(r"#[0-9a-fA-F]{3,8}|[a-zA-Z]{1,24}|rgba?\([0-9.,% ]+\)", value):
        raise ValueError(f"cor inválida: {value}")
    return value


class LipiError(Exception):
    pass


class Lipi:
    def __init__(self):
        self.mode: Optional[str] = None
        self.title = "Projeto Lipi"
        self.background = "#101020"
        self.text_color = "#ffffff"
        self.elements: List[str] = []
        self.styles: List[str] = []
        self.scripts: List[str] = []
        self.game_objects: List[str] = []
        self.click_action: Optional[str] = None

    def reset(self):
        self.__init__()

    def compile_file(self, source: Path, output: Optional[Path] = None) -> Path:
        try:
            code = source.read_text(encoding="utf-8")
        except OSError as exc:
            raise LipiError(f"não consegui ler {source}: {exc}") from exc
        return self.compile(code, output or source.with_suffix(".html"))

    def compile(self, code: str, output: Path) -> Path:
        self.reset()
        lines = code.splitlines()
        in_click = False
        click_lines: List[str] = []

        for number, original in enumerate(lines, 1):
            line = original.strip()
            if not line or line.startswith("#"):
                continue

            if in_click:
                if line.lower() == "fim":
                    self.click_action = "\n".join(click_lines)
                    in_click = False
                    click_lines = []
                else:
                    click_lines.append(line)
                continue

            if line.lower() == "ao clicar:":
                in_click = True
                continue

            try:
                self.parse_line(line)
            except (ValueError, LipiError) as exc:
                raise LipiError(f"linha {number}: {exc}") from exc

        if in_click:
            raise LipiError("bloco 'ao clicar:' sem 'fim'.")

        if self.mode not in ("site", "jogo"):
            raise LipiError("comece o arquivo com: site \"Nome\" ou jogo \"Nome\".")

        output.parent.mkdir(parents=True, exist_ok=True)
        document = self.render_site() if self.mode == "site" else self.render_game()
        output.write_text(document, encoding="utf-8")
        return output

    def parse_line(self, line: str):
        parts = line.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if command in ("site", "jogo"):
            if self.mode is not None:
                raise LipiError("use apenas um comando inicial: site ou jogo.")
            self.mode = command
            self.title = value_of(arg) if arg else "Projeto Lipi"
            return

        if self.mode is None:
            raise LipiError("o primeiro comando deve ser site ou jogo.")

        if command == "fundo":
            self.background = safe_color(arg)
        elif command == "cor_texto":
            self.text_color = safe_color(arg)
        elif command == "titulo":
            self.elements.append(f"<h1>{html.escape(value_of(arg))}</h1>")
        elif command == "texto":
            self.elements.append(f"<p>{html.escape(value_of(arg))}</p>")
        elif command == "botao":
            label = html.escape(value_of(arg))
            self.elements.append(f'<button class="lipi-button" id="lipi-action">{label}</button>')
        elif command == "imagem":
            url = value_of(arg)
            if not re.match(r"^https://", url):
                raise ValueError("imagem deve usar um endereço HTTPS.")
            self.elements.append(
                f'<img class="lipi-image" src="{html.escape(url, quote=True)}" alt="Imagem do projeto">'
            )
        elif command == "espacamento":
            self.styles.append(f".lipi-content{{gap:{int(arg)}px}}")
        elif command == "arredondar":
            self.styles.append(f".lipi-button{{border-radius:{int(arg)}px}}")
        elif command == "animacao":
            effect = value_of(arg).lower()
            if effect == "crescer":
                self.styles.append(".lipi-button:hover{transform:scale(1.07)}")
            elif effect == "brilhar":
                self.styles.append(".lipi-button:hover{box-shadow:0 0 22px #3994ff}")
            else:
                raise ValueError("animação disponível: crescer ou brilhar.")
        elif command == "cenario":
            if self.mode != "jogo":
                raise ValueError("'cenario' só pode ser usado em jogo.")
            self.background = safe_color(arg)
        elif command == "chao":
            if self.mode != "jogo":
                raise ValueError("'chao' só pode ser usado em jogo.")
            self.game_objects.append(
                f"addGround({json_string(safe_color(arg))});"
            )
        elif command == "cubo":
            if self.mode != "jogo":
                raise ValueError("'cubo' só pode ser usado em jogo.")
            values = arg.split()
            if len(values) != 4:
                raise ValueError('use: cubo X Y Z cor (ex.: cubo 0 1 0 azul)')
            x, y, z = (float(v) for v in values[:3])
            color = safe_color(values[3])
            self.game_objects.append(
                f"addCube({x}, {y}, {z}, {json_string(color)});"
            )
        elif command == "jogador":
            if self.mode != "jogo":
                raise ValueError("'jogador' só pode ser usado em jogo.")
            self.game_objects.append("addPlayer();")
        elif command == "fim":
            return
        else:
            raise ValueError(f"comando desconhecido: {command}")

    def render_site(self) -> str:
        click_js = ""
        if self.click_action:
            # Na primeira versão, o bloco aceita apenas mostrar "mensagem".
            match = re.fullmatch(r"""mostrar\s+(['"])(.*?)\1""", self.click_action, re.S)
            if not match:
                raise LipiError("por enquanto, 'ao clicar' aceita: mostrar \"mensagem\".")
            click_js = "alert(" + json_string(match.group(2)) + ");"

        styles = "\n".join(self.styles)
        body = "\n".join(self.elements)
        action = ""
        if click_js:
            action = f"""const button = document.getElementById('lipi-action');
if (button) button.addEventListener('click', () => {{ {click_js} }});"""
        return f"""<!doctype html>
<html lang="pt-br">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(self.title)}</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;min-height:100vh;padding:48px 20px;background:{self.background};
color:{self.text_color};font-family:Arial,sans-serif}}
.lipi-content{{max-width:900px;margin:auto;display:flex;flex-direction:column;
align-items:center;gap:18px;text-align:center}}
h1{{font-size:clamp(30px,5vw,52px);margin:0}}
p{{font-size:18px;line-height:1.6;color:inherit}}
.lipi-button{{padding:14px 26px;border:0;border-radius:12px;background:#1677ff;
color:white;font-size:16px;cursor:pointer;transition:transform .2s,box-shadow .2s}}
.lipi-image{{max-width:min(100%,700px);height:auto;border-radius:14px}}
{styles}
</style>
</head>
<body>
<main class="lipi-content">
{body}
</main>
<script>{action}</script>
</body>
</html>"""

    def render_game(self) -> str:
        objects = "\n".join(self.game_objects)
        return f"""<!doctype html>
<html lang="pt-br">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(self.title)}</title>
<style>html,body{{margin:0;width:100%;height:100%;overflow:hidden}}canvas{{display:block}}</style>
</head>
<body>
<script type="module">
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';
const scene = new THREE.Scene();
scene.background = new THREE.Color({json_string(self.background)});
const camera = new THREE.PerspectiveCamera(70, innerWidth/innerHeight, 0.1, 1000);
camera.position.set(5,5,8); camera.lookAt(0,0,0);
const renderer = new THREE.WebGLRenderer({{antialias:true}});
renderer.setSize(innerWidth,innerHeight); renderer.setPixelRatio(devicePixelRatio);
document.body.appendChild(renderer.domElement);
scene.add(new THREE.HemisphereLight(0xffffff,0x555555,2));
const light = new THREE.DirectionalLight(0xffffff,2); light.position.set(4,8,5); scene.add(light);
function addCube(x,y,z,color) {{
 const mesh = new THREE.Mesh(new THREE.BoxGeometry(1,1,1),
 new THREE.MeshStandardMaterial({{color}}));
 mesh.position.set(x,y,z); scene.add(mesh);
}}
function addGround(color) {{
 const mesh = new THREE.Mesh(new THREE.PlaneGeometry(100,100),
 new THREE.MeshStandardMaterial({{color}}));
 mesh.rotation.x=-Math.PI/2; mesh.position.y=-0.51; scene.add(mesh);
}}
function addPlayer() {{
 const mesh = new THREE.Mesh(new THREE.CapsuleGeometry(0.35,0.8,4,8),
 new THREE.MeshStandardMaterial({{color:'#ffcc33'}}));
 mesh.position.y=0.2; scene.add(mesh);
}}
{objects}
function animate() {{ requestAnimationFrame(animate); renderer.render(scene,camera); }}
animate();
addEventListener('resize',()=>{{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight);}});
</script>
</body>
</html>"""


def json_string(value: str) -> str:
    import json
    return json.dumps(value, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Compilador inicial da linguagem Lipi.")
    parser.add_argument("arquivo", nargs="?", help="arquivo .lp para compilar")
    parser.add_argument("-o", "--saida", help="arquivo HTML de saída")
    parser.add_argument("--versao", action="version", version=f"Lipi {VERSION}")
    args = parser.parse_args()

    if not args.arquivo:
        parser.print_help()
        return 2

    source = Path(args.arquivo)
    if source.suffix.lower() != ".lp":
        print("Erro: os programas Lipi devem terminar em .lp", file=sys.stderr)
        return 2

    output = Path(args.saida) if args.saida else source.with_suffix(".html")
    try:
        result = Lipi().compile_file(source, output)
    except (LipiError, OSError, ValueError) as exc:
        print(f"Erro Lipi: {exc}", file=sys.stderr)
        return 1
    print(f"Lipi {VERSION}: arquivo criado em {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
