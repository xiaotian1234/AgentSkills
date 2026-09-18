#!/usr/bin/env python3
"""Render a vertical tutorial long image from Markdown-like text or JSON.

The script is intentionally deterministic: it preserves user-provided text and
places local screenshots without generative alteration.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError as exc:  # pragma: no cover - environment dependent
    raise SystemExit(
        "Pillow is required. Install with: python -m pip install pillow"
    ) from exc


@dataclass
class Step:
    title: str
    body: str = ""
    image: str = ""


@dataclass
class Spec:
    title: str
    subtitle: str
    width: int
    theme: str
    steps: list[Step]


LIGHT = {
    "bg": (245, 247, 251),
    "card": (255, 255, 255),
    "text": (20, 28, 45),
    "muted": (88, 99, 122),
    "line": (224, 229, 238),
    "accent": (37, 99, 235),
    "accent_text": (255, 255, 255),
    "shadow": (213, 219, 230),
    "missing_bg": (255, 247, 237),
    "missing_text": (154, 52, 18),
}

DARK = {
    "bg": (15, 23, 42),
    "card": (30, 41, 59),
    "text": (241, 245, 249),
    "muted": (203, 213, 225),
    "line": (71, 85, 105),
    "accent": (96, 165, 250),
    "accent_text": (15, 23, 42),
    "shadow": (2, 6, 23),
    "missing_bg": (69, 26, 3),
    "missing_text": (254, 215, 170),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Markdown-like or JSON tutorial spec")
    parser.add_argument("output", help="Output PNG path")
    parser.add_argument("--width", type=int, default=None, help="Canvas width in pixels")
    parser.add_argument("--theme", choices=["light", "dark"], default=None)
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8")


def parse_spec(path: Path, width: int | None, theme: str | None) -> Spec:
    text = read_text(path)
    if path.suffix.lower() == ".json":
        raw = json.loads(text)
        spec = parse_json_spec(raw)
    else:
        try:
            raw = json.loads(text)
            spec = parse_json_spec(raw)
        except json.JSONDecodeError:
            spec = parse_markdown_spec(text)

    if width:
        spec.width = width
    if theme:
        spec.theme = theme
    spec.width = max(720, min(2160, int(spec.width or 1080)))
    spec.theme = "dark" if spec.theme.lower() == "dark" else "light"
    return spec


def parse_json_spec(raw: dict[str, Any]) -> Spec:
    steps = []
    for item in raw.get("steps", []):
        steps.append(
            Step(
                title=str(item.get("title") or item.get("step") or "").strip(),
                body=str(item.get("body") or item.get("description") or item.get("说明") or "").strip(),
                image=str(item.get("image") or item.get("图片") or "").strip(),
            )
        )
    return Spec(
        title=str(raw.get("title") or raw.get("标题") or "操作步骤").strip(),
        subtitle=str(raw.get("subtitle") or raw.get("副标题") or "").strip(),
        width=int(raw.get("width") or raw.get("宽度") or 1080),
        theme=str(raw.get("theme") or raw.get("主题") or "light").strip(),
        steps=[step for step in steps if step.title or step.body or step.image],
    )


def parse_markdown_spec(text: str) -> Spec:
    title = "操作步骤"
    subtitle = ""
    width = 1080
    theme = "light"
    steps: list[Step] = []
    current: Step | None = None

    step_re = re.compile(r"^\s*(?:步骤|Step)\s*(\d+)?\s*[：:.-]\s*(.*)\s*$", re.I)

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        key, value = split_key_value(line)
        normalized_key = key.lower()

        if normalized_key in {"标题", "title"}:
            title = value or title
            continue
        if normalized_key in {"副标题", "subtitle"}:
            subtitle = value
            continue
        if normalized_key in {"宽度", "width"}:
            width = parse_int(value, width)
            continue
        if normalized_key in {"主题", "theme"}:
            theme = value or theme
            continue

        match = step_re.match(line)
        if match:
            if current:
                steps.append(current)
            current = Step(title=match.group(2).strip())
            continue

        if normalized_key in {"说明", "描述", "body", "description", "caption"}:
            if current is None:
                current = Step(title="")
            current.body = join_text(current.body, value)
            continue
        if normalized_key in {"图片", "图", "image", "screenshot", "截图"}:
            if current is None:
                current = Step(title="")
            current.image = value.strip().strip('"')
            continue

        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            if title == "操作步骤":
                title = heading
            elif current:
                current.body = join_text(current.body, heading)
            continue

        if current is None:
            if title == "操作步骤":
                title = line
            else:
                subtitle = join_text(subtitle, line)
        else:
            current.body = join_text(current.body, line)

    if current:
        steps.append(current)
    return Spec(title=title, subtitle=subtitle, width=width, theme=theme, steps=steps)


def split_key_value(line: str) -> tuple[str, str]:
    for sep in ("：", ":"):
        if sep in line:
            key, value = line.split(sep, 1)
            return key.strip(), value.strip()
    return line.strip(), ""


def parse_int(value: str, default: int) -> int:
    try:
        return int(re.sub(r"[^\d]", "", value))
    except ValueError:
        return default


def join_text(existing: str, value: str) -> str:
    if not value:
        return existing
    return f"{existing}\n{value}" if existing else value


def find_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    windir = os.environ.get("WINDIR", r"C:\Windows")
    if bold:
        candidates.extend(
            [
                Path(windir) / "Fonts" / "msyhbd.ttc",
                Path(windir) / "Fonts" / "simhei.ttf",
                Path(windir) / "Fonts" / "arialbd.ttf",
            ]
        )
    candidates.extend(
        [
            Path(windir) / "Fonts" / "msyh.ttc",
            Path(windir) / "Fonts" / "simhei.ttf",
            Path(windir) / "Fonts" / "arial.ttf",
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        ]
    )
    for candidate in candidates:
        if candidate.exists():
            try:
                return ImageFont.truetype(str(candidate), size)
            except OSError:
                continue
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=8)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> str:
    wrapped_lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        if not paragraph:
            wrapped_lines.append("")
            continue
        current = ""
        for char in paragraph:
            trial = current + char
            if text_size(draw, trial, font)[0] <= max_width or not current:
                current = trial
            else:
                wrapped_lines.append(current)
                current = char
        if current:
            wrapped_lines.append(current)
    return "\n".join(wrapped_lines)


def rounded_rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill: tuple[int, int, int]) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def card_height(
    draw: ImageDraw.ImageDraw,
    spec: Spec,
    step: Step,
    palette: dict[str, tuple[int, int, int]],
    content_width: int,
    fonts: dict[str, ImageFont.ImageFont],
) -> tuple[int, str, str, tuple[int, int] | None, bool]:
    title_text = wrap_text(draw, step.title, fonts["step_title"], content_width - 112)
    body_text = wrap_text(draw, step.body, fonts["body"], content_width - 40) if step.body else ""
    _, title_h = text_size(draw, title_text or " ", fonts["step_title"])
    _, body_h = text_size(draw, body_text, fonts["body"]) if body_text else (0, 0)

    image_size = None
    image_exists = False
    if step.image:
        image_path = Path(step.image)
        if image_path.exists():
            try:
                with Image.open(image_path) as img:
                    image_exists = True
                    max_image_w = content_width - 40
                    ratio = max_image_w / img.width
                    image_size = (max_image_w, max(1, math.ceil(img.height * ratio)))
            except OSError:
                image_size = (content_width - 40, 96)
        else:
            image_size = (content_width - 40, 96)

    height = 34 + max(54, title_h) + 18 + body_h
    if body_h:
        height += 18
    if image_size:
        height += image_size[1] + 24
    height += 30
    return height, title_text, body_text, image_size, image_exists


def render(spec: Spec, output: Path) -> None:
    palette = DARK if spec.theme == "dark" else LIGHT
    width = spec.width
    margin = round(width * 0.055)
    gap = 26
    content_width = width - 2 * margin

    fonts = {
        "title": find_font(round(width * 0.046), bold=True),
        "subtitle": find_font(round(width * 0.023)),
        "step_title": find_font(round(width * 0.031), bold=True),
        "body": find_font(round(width * 0.023)),
        "badge": find_font(round(width * 0.025), bold=True),
        "footer": find_font(round(width * 0.018)),
    }

    probe = Image.new("RGB", (width, 200), palette["bg"])
    draw = ImageDraw.Draw(probe)
    title_wrapped = wrap_text(draw, spec.title, fonts["title"], content_width)
    subtitle_wrapped = wrap_text(draw, spec.subtitle, fonts["subtitle"], content_width) if spec.subtitle else ""
    _, title_h = text_size(draw, title_wrapped, fonts["title"])
    _, subtitle_h = text_size(draw, subtitle_wrapped, fonts["subtitle"]) if subtitle_wrapped else (0, 0)

    prepared = [
        card_height(draw, spec, step, palette, content_width, fonts) for step in spec.steps
    ]

    header_h = margin + title_h + (subtitle_h + 20 if subtitle_h else 0) + 36
    total_h = header_h + sum(item[0] for item in prepared) + gap * max(0, len(prepared) - 1) + margin + 36
    img = Image.new("RGB", (width, total_h), palette["bg"])
    draw = ImageDraw.Draw(img)

    y = margin
    draw.multiline_text((margin, y), title_wrapped, font=fonts["title"], fill=palette["text"], spacing=10)
    y += title_h + 14
    if subtitle_wrapped:
        draw.multiline_text((margin, y), subtitle_wrapped, font=fonts["subtitle"], fill=palette["muted"], spacing=8)
        y += subtitle_h + 24
    else:
        y += 14

    for index, step in enumerate(spec.steps, start=1):
        height, title_text, body_text, image_size, image_exists = prepared[index - 1]
        x = margin
        draw.rounded_rectangle(
            (x + 4, y + 6, x + content_width + 4, y + height + 6),
            radius=28,
            fill=palette["shadow"],
        )
        rounded_rect(draw, (x, y, x + content_width, y + height), 28, palette["card"])

        inner_x = x + 28
        inner_y = y + 30
        badge_size = 56
        draw.rounded_rectangle(
            (inner_x, inner_y, inner_x + badge_size, inner_y + badge_size),
            radius=18,
            fill=palette["accent"],
        )
        badge_text = str(index)
        bw, bh = text_size(draw, badge_text, fonts["badge"])
        draw.text(
            (inner_x + (badge_size - bw) / 2, inner_y + (badge_size - bh) / 2 - 2),
            badge_text,
            font=fonts["badge"],
            fill=palette["accent_text"],
        )

        text_x = inner_x + badge_size + 24
        draw.multiline_text(
            (text_x, inner_y + 2),
            title_text or f"步骤 {index}",
            font=fonts["step_title"],
            fill=palette["text"],
            spacing=8,
        )
        _, step_title_h = text_size(draw, title_text or f"步骤 {index}", fonts["step_title"])
        cursor_y = inner_y + max(badge_size, step_title_h) + 18

        if body_text:
            draw.multiline_text(
                (inner_x, cursor_y),
                body_text,
                font=fonts["body"],
                fill=palette["muted"],
                spacing=9,
            )
            _, body_h = text_size(draw, body_text, fonts["body"])
            cursor_y += body_h + 22

        if image_size:
            image_x = inner_x
            image_y = cursor_y
            image_w, image_h = image_size
            if image_exists:
                try:
                    with Image.open(Path(step.image)) as step_img:
                        step_img = ImageOps.exif_transpose(step_img).convert("RGB")
                        step_img.thumbnail((image_w, image_h), Image.Resampling.LANCZOS)
                        framed = Image.new("RGB", (image_w, image_h), palette["line"])
                        paste_x = (image_w - step_img.width) // 2
                        paste_y = (image_h - step_img.height) // 2
                        framed.paste(step_img, (paste_x, paste_y))
                        img.paste(framed, (image_x, image_y))
                except OSError:
                    draw_missing(draw, image_x, image_y, image_w, image_h, step.image, palette, fonts["body"])
            else:
                draw_missing(draw, image_x, image_y, image_w, image_h, step.image, palette, fonts["body"])
            draw.rounded_rectangle(
                (image_x, image_y, image_x + image_w, image_y + image_h),
                radius=18,
                outline=palette["line"],
                width=2,
            )

        y += height + gap

    footer = "Generated by tutorial-long-image"
    fw, fh = text_size(draw, footer, fonts["footer"])
    draw.text(((width - fw) / 2, total_h - margin), footer, font=fonts["footer"], fill=palette["muted"])

    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output)


def draw_missing(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    h: int,
    path: str,
    palette: dict[str, tuple[int, int, int]],
    font: ImageFont.ImageFont,
) -> None:
    draw.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=palette["missing_bg"])
    message = wrap_text(draw, f"图片不可读取：{path}", font, w - 40)
    draw.multiline_text((x + 22, y + 24), message, font=font, fill=palette["missing_text"], spacing=8)


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.exists():
        print(f"Input not found: {input_path}", file=sys.stderr)
        return 2
    spec = parse_spec(input_path, args.width, args.theme)
    if not spec.steps:
        print("No steps found in input.", file=sys.stderr)
        return 2
    render(spec, output_path)
    print(json.dumps({"output": str(output_path), "width": spec.width, "steps": len(spec.steps)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

