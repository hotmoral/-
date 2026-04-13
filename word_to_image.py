#!/usr/bin/env python3
"""입력 텍스트를 픽셀 아트 BMP 이미지로 만드는 CLI/GUI 프로그램 (외부 라이브러리 불필요)."""

from __future__ import annotations

import argparse
import struct
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

# 5x7 비트맵 폰트 (필요한 문자만 확장 가능)
FONT_5X7 = {
    "A": [0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    "B": [0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110],
    "C": [0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110],
    "D": [0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110],
    "E": [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111],
    "F": [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000],
    "G": [0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01110],
    "H": [0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    "I": [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b11111],
    "J": [0b00111, 0b00010, 0b00010, 0b00010, 0b10010, 0b10010, 0b01100],
    "K": [0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001],
    "L": [0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111],
    "M": [0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001],
    "N": [0b10001, 0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001],
    "O": [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "P": [0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000],
    "Q": [0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101],
    "R": [0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001],
    "S": [0b01111, 0b10000, 0b10000, 0b01110, 0b00001, 0b00001, 0b11110],
    "T": [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
    "U": [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "V": [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
    "W": [0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b10101, 0b01010],
    "X": [0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001],
    "Y": [0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100],
    "Z": [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111],
    "0": [0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110],
    "1": [0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    "2": [0b01110, 0b10001, 0b00001, 0b00110, 0b01000, 0b10000, 0b11111],
    "3": [0b11110, 0b00001, 0b00001, 0b01110, 0b00001, 0b00001, 0b11110],
    "4": [0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010],
    "5": [0b11111, 0b10000, 0b10000, 0b11110, 0b00001, 0b00001, 0b11110],
    "6": [0b01110, 0b10000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110],
    "7": [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000],
    "8": [0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
    "9": [0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00001, 0b01110],
    " ": [0, 0, 0, 0, 0, 0, 0],
}


def parse_color(s: str) -> tuple[int, int, int]:
    parts = [int(x.strip()) for x in s.split(",")]
    if len(parts) != 3 or any(not (0 <= p <= 255) for p in parts):
        raise ValueError("색상은 0~255 범위의 R,G,B 형식이어야 합니다.")
    return parts[0], parts[1], parts[2]


def glyph_for_char(ch: str) -> list[int]:
    upper = ch.upper()
    if upper in FONT_5X7:
        return FONT_5X7[upper]

    # 폰트에 없는 문자(예: 한글)는 코드포인트 기반 패턴으로 대체
    code = ord(ch)
    rows = []
    for r in range(7):
        pattern = ((code >> r) ^ (code >> (r + 3)) ^ (code >> (r + 5))) & 0b11111
        rows.append(pattern or 0b00100)
    return rows


def draw_text_pixels(text: str, scale: int, padding: int) -> list[list[int]]:
    glyph_w, glyph_h = 5, 7
    spacing = 1
    text_w = len(text) * (glyph_w + spacing) - spacing

    canvas_w = text_w * scale + padding * 2
    canvas_h = glyph_h * scale + padding * 2
    pixels = [[0 for _ in range(canvas_w)] for _ in range(canvas_h)]

    cursor_x = padding
    for ch in text:
        glyph = glyph_for_char(ch)
        for gy, row_bits in enumerate(glyph):
            for gx in range(glyph_w):
                if row_bits & (1 << (glyph_w - 1 - gx)):
                    for sy in range(scale):
                        for sx in range(scale):
                            px = cursor_x + gx * scale + sx
                            py = padding + gy * scale + sy
                            pixels[py][px] = 1
        cursor_x += (glyph_w + spacing) * scale

    return pixels


def write_bmp(path: Path, pixels: list[list[int]], fg: tuple[int, int, int], bg: tuple[int, int, int]) -> None:
    height = len(pixels)
    width = len(pixels[0]) if height else 0
    row_stride = ((width * 3 + 3) // 4) * 4
    pixel_data_size = row_stride * height
    offset = 14 + 40
    file_size = offset + pixel_data_size

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        f.write(b"BM")
        f.write(struct.pack("<IHHI", file_size, 0, 0, offset))
        f.write(struct.pack("<IIIHHIIIIII", 40, width, height, 1, 24, 0, pixel_data_size, 2835, 2835, 0, 0))

        pad = b"\x00" * (row_stride - width * 3)
        for y in range(height - 1, -1, -1):
            row = bytearray()
            for x in range(width):
                color = fg if pixels[y][x] else bg
                r, g, b = color
                row.extend([b, g, r])
            f.write(row)
            f.write(pad)


def generate_image(text: str, output: str, scale: int, padding: int, foreground: str, background: str) -> Path:
    if not text.strip():
        raise ValueError("텍스트를 입력해 주세요.")
    if scale <= 0:
        raise ValueError("--scale 은 1 이상이어야 합니다.")
    if padding < 0:
        raise ValueError("--padding 은 0 이상이어야 합니다.")

    pixels = draw_text_pixels(text, scale, padding)
    output_path = Path(output)
    write_bmp(output_path, pixels, parse_color(foreground), parse_color(background))
    return output_path


def launch_gui() -> None:
    root = tk.Tk()
    root.title("Word to Image - BMP 생성기")
    root.geometry("500x290")

    vars_ = {
        "text": tk.StringVar(value="안녕하세요"),
        "output": tk.StringVar(value="output.bmp"),
        "scale": tk.StringVar(value="20"),
        "padding": tk.StringVar(value="30"),
        "foreground": tk.StringVar(value="255,230,0"),
        "background": tk.StringVar(value="30,30,30"),
        "status": tk.StringVar(value="값을 입력하고 [이미지 생성]을 눌러 주세요."),
    }

    def browse_output() -> None:
        filename = filedialog.asksaveasfilename(
            title="저장할 BMP 파일 선택",
            defaultextension=".bmp",
            filetypes=[("Bitmap", "*.bmp")],
        )
        if filename:
            vars_["output"].set(filename)

    def on_generate() -> None:
        try:
            out = generate_image(
                text=vars_["text"].get(),
                output=vars_["output"].get(),
                scale=int(vars_["scale"].get()),
                padding=int(vars_["padding"].get()),
                foreground=vars_["foreground"].get(),
                background=vars_["background"].get(),
            )
            vars_["status"].set(f"완료: {out}")
            messagebox.showinfo("성공", f"이미지를 생성했습니다.\n{out}")
        except Exception as e:
            vars_["status"].set(f"오류: {e}")
            messagebox.showerror("생성 실패", str(e))

    fields = [
        ("텍스트", "text"),
        ("출력 경로", "output"),
        ("배율(scale)", "scale"),
        ("여백(padding)", "padding"),
        ("글자색 (R,G,B)", "foreground"),
        ("배경색 (R,G,B)", "background"),
    ]

    for idx, (label, key) in enumerate(fields):
        tk.Label(root, text=label, anchor="w").grid(row=idx, column=0, sticky="w", padx=10, pady=4)
        tk.Entry(root, textvariable=vars_[key], width=40).grid(row=idx, column=1, sticky="we", padx=6, pady=4)

    tk.Button(root, text="찾아보기", command=browse_output).grid(row=1, column=2, padx=6)
    tk.Button(root, text="이미지 생성", command=on_generate, height=2).grid(row=7, column=0, columnspan=3, pady=12)
    tk.Label(root, textvariable=vars_["status"], fg="#1a1a1a").grid(row=8, column=0, columnspan=3, padx=10, sticky="w")

    root.columnconfigure(1, weight=1)
    root.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser(description="입력 단어를 픽셀 아트 BMP 이미지로 생성합니다.")
    parser.add_argument("text", nargs="?", help="이미지로 만들 단어/문장")
    parser.add_argument("--output", default="output.bmp", help="출력 파일 경로 (.bmp)")
    parser.add_argument("--scale", type=int, default=20, help="픽셀 확대 배율 (기본 20)")
    parser.add_argument("--padding", type=int, default=30, help="이미지 내부 여백")
    parser.add_argument("--foreground", default="255,230,0", help="글자색 R,G,B")
    parser.add_argument("--background", default="30,30,30", help="배경색 R,G,B")
    parser.add_argument("--gui", action="store_true", help="GUI 창으로 실행")
    args = parser.parse_args()

    if args.gui or not args.text:
        launch_gui()
        return

    out = generate_image(
        text=args.text,
        output=args.output,
        scale=args.scale,
        padding=args.padding,
        foreground=args.foreground,
        background=args.background,
    )
    print(f"이미지 생성 완료: {out}")


if __name__ == "__main__":
    main()
