"""Gera o ícone do app (PNG 192x192) sem depender de bibliotecas externas.

Roda no GitHub Actions antes do build, porque o repositório guarda só arquivos de texto.
"""
import os
import struct
import zlib

SAIDA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "app", "src", "main", "res", "mipmap-xxxhdpi", "ic_launcher.png",
)
TAMANHO = 192


def bloco(tipo, dados):
    return (struct.pack(">I", len(dados)) + tipo + dados
            + struct.pack(">I", zlib.crc32(tipo + dados) & 0xffffffff))


def pixel(x, y, w, h):
    u = (x + 0.5) / w
    v = (y + 0.5) / h
    t = (u + v) / 2
    fundo = (int(123 + (241 - 123) * t), int(47 + (7 - 47) * t), int(247 + (163 - 247) * t))
    if (u - 0.78) ** 2 + (v - 0.22) ** 2 < 0.08 ** 2:
        return (231, 76, 60)
    if 0.22 <= u <= 0.78 and 0.36 <= v <= 0.68:
        d = (u - 0.5) ** 2 + (v - 0.52) ** 2
        if d < 0.13 ** 2:
            return (120, 200, 255) if d < 0.07 ** 2 else (34, 34, 34)
        return (255, 255, 255)
    return fundo


def main():
    linhas = bytearray()
    for y in range(TAMANHO):
        linhas.append(0)
        for x in range(TAMANHO):
            linhas += bytes(pixel(x, y, TAMANHO, TAMANHO))
    png = (b"\x89PNG\r\n\x1a\n"
           + bloco(b"IHDR", struct.pack(">IIBBBBB", TAMANHO, TAMANHO, 8, 2, 0, 0, 0))
           + bloco(b"IDAT", zlib.compress(bytes(linhas), 9))
           + bloco(b"IEND", b""))
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "wb") as f:
        f.write(png)
    print("Ícone gerado:", os.path.normpath(SAIDA), len(png), "bytes")


if __name__ == "__main__":
    main()
