---
name: tutorial-long-image
description: Create deterministic vertical tutorial long images from operation steps, captions, and local screenshots. Use when the user asks for 教程长图、操作步骤长图、图文步骤卡片、把步骤文字和图片集中到一张长图、thumbnail/cover-style step collage with exact text.
license: MIT
metadata:
  short-description: Turn steps and screenshots into one long tutorial PNG
---

# Tutorial Long Image

Create a readable vertical PNG that combines operation steps, short explanations, and screenshots. Prefer deterministic layout over generative image creation so the user's text remains exact and screenshots are not distorted.

## When To Use

Use this skill when the user wants:

- A single long image from step-by-step text and screenshots.
- A phone-friendly tutorial card, SOP image, Feishu/WeChat sharing image, or operation guide.
- A thumbnail-like cover plus ordered steps, where exact text and real screenshots matter.

Do not use image generation as the primary path when the image must preserve exact Chinese/English text, UI screenshots, code, menu names, or file paths. Use image generation only for optional decorative backgrounds when the user explicitly accepts possible text/image variation.

## Input Contract

Accept either natural language or a simple spec. If the user provides image paths outside the current readable workspace, request read permission before rendering.

Recommended spec:

```text
标题：XXX 操作教程
副标题：可选说明
宽度：1080
主题：light

步骤1：打开软件
说明：确认主界面已经加载完成
图片：D:\path\step1.png

步骤2：点击设置
图片：D:\path\step2.png
```

Also accept JSON with:

```json
{
  "title": "XXX 操作教程",
  "subtitle": "可选说明",
  "width": 1080,
  "theme": "light",
  "steps": [
    {"title": "打开软件", "body": "确认主界面已经加载完成", "image": "D:\\path\\step1.png"}
  ]
}
```

## Workflow

1. Preserve the user's wording exactly. Do not rewrite UI labels, command names, code, menu paths, or numbered steps unless the user asks for polishing.
2. Normalize the input into a temporary Markdown or JSON spec.
3. Render with `scripts/render_tutorial_long_image.py` when filesystem and Python/Pillow are available.
4. Save the PNG into the current workspace or the user's requested output directory. Do not overwrite an existing file unless the user explicitly asks to replace it; use a versioned name instead.
5. Inspect the output when possible and report the saved path.

Default style:

- Width `1080px`, vertical canvas, light background.
- Title card at top, then one card per step.
- Each step has a numbered badge, title, optional body text, and optional screenshot.
- Screenshots keep aspect ratio and are never cropped unless the user asks.
- Long images may be very tall; split into multiple PNGs only when the user asks or when a target platform has a size limit.

## Script

Use:

```bash
python scripts/render_tutorial_long_image.py <input.md-or-json> <output.png>
```

Useful options:

```bash
python scripts/render_tutorial_long_image.py spec.md output.png --width 1080 --theme light
python scripts/render_tutorial_long_image.py spec.json output.png --width 1440 --theme dark
```

The script requires Pillow. If Pillow is unavailable, install it in the active Python environment or fall back to generating an HTML/CSS layout and capturing it with a browser screenshot.

## Quality Checks

Before final response, verify:

- The output PNG exists and has nonzero size.
- Every provided step appears in order.
- Every provided screenshot path that exists was placed or explicitly reported as missing.
- Text remains selectable in the source spec and visually readable in the PNG.
- Screenshots are not stretched, cropped, or rotated unexpectedly.

