---
name: markitdown
description: 将任意文件（Word、PDF、Excel、PowerPoint、HTML、图片、扫描件、截图等）转换为 Markdown 格式，输出到源文件同目录。图片/扫描件/截图优先使用 RapidOCR 离线识别。触发词：转成md、转换md、转为markdown、convert to md、to markdown、markitdown。
---

# markitdown 文件转 Markdown Skill

## 触发条件

当用户：
- 提到某个文件并说"转成md"、"转为markdown"、"转换成md"、"to markdown"、"convert to md"
- 直接引用文件路径并要求转换格式
- 说"把这个文件转成md"、"转换成markdown"
- 提到扫描件、截图、图片需要识别文字

## 环境信息

- **Python路径：** `D:\Install\Anaconda\python.exe`
- **markitdown：** 已安装（通用文档转换）
- **rapidocr + onnxruntime：** 已安装（图片/扫描件离线OCR，支持中英文，无需API Key）

## 文件类型与转换策略

| 类型 | 扩展名 | 转换策略 |
|------|--------|----------|
| 图片/截图/扫描件 | .jpg .jpeg .png .gif .bmp .webp .tiff .tif | **RapidOCR** → 离线OCR识别文字 |
| PDF（文字版） | .pdf | markitdown → 若结果稀少则提示可能是扫描版 |
| Word | .docx .doc | markitdown |
| Excel | .xlsx .xls | markitdown |
| PowerPoint | .pptx .ppt | markitdown |
| HTML/网页 | .html .htm | markitdown |
| 音频（转录） | .mp3 .wav .m4a | markitdown（需OpenAI API Key）|
| CSV / JSON / XML | .csv .json .xml | markitdown |
| 纯文本 | .txt | markitdown |

## 执行步骤

### 第一步：提取文件路径

从用户消息中识别文件路径。规则：
- 用户直接粘贴路径：`E:\docs\report.docx`
- 用户说"这个文件"→ 检查 IDE 当前打开的文件（ide_opened_file 标签）
- 相对路径 → 相对当前工作目录解析

**无法确定路径时直接问用户，不要猜测。**

### 第二步：确认文件存在 + 判断策略

```powershell
$filePath = "FILE_PATH"
if (Test-Path $filePath) {
    $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
    $dir = Split-Path $filePath -Parent
    $basename = [System.IO.Path]::GetFileNameWithoutExtension($filePath)
    $outputPath = Join-Path $dir "$basename.md"
    Write-Host "文件: $filePath"
    Write-Host "输出: $outputPath"
    Write-Host "扩展名: $ext"
} else {
    Write-Host "错误：文件不存在 $filePath"
}
```

根据扩展名选择策略：
- `.jpg .jpeg .png .gif .bmp .webp .tiff .tif` → 走**RapidOCR路径**（第三步A）
- 其他格式 → 走**markitdown路径**（第三步B）

---

### 第三步A：图片/截图/扫描件 → RapidOCR

```powershell
$python = "D:\Install\Anaconda\python.exe"

& $python -c @"
from rapidocr import RapidOCR
from pathlib import Path
import sys

try:
    engine = RapidOCR()
    result = engine(r'SOURCE_FILE_PATH')
    
    if not result.txts:
        print('警告：未识别到任何文字，可能图片质量太低或不含文字', file=sys.stderr)
        text_content = '<!-- RapidOCR 未识别到文字内容 -->\n'
    else:
        lines = list(result.txts)
        text_content = '\n'.join(lines)
    
    output = Path(r'OUTPUT_MD_PATH')
    output.write_text(text_content, encoding='utf-8')
    print(f'OCR完成：共识别 {len(result.txts) if result.txts else 0} 行文字')
    print(f'内容长度：{len(text_content)} 字符')
    print(f'输出文件：{output}')
except Exception as e:
    print(f'错误: {e}', file=sys.stderr)
    sys.exit(1)
"@
```

替换 `SOURCE_FILE_PATH` 和 `OUTPUT_MD_PATH` 为实际路径。

---

### 第三步B：其他格式 → markitdown

```powershell
$python = "D:\Install\Anaconda\python.exe"

& $python -c @"
from markitdown import MarkItDown
from pathlib import Path
import sys

try:
    md = MarkItDown()
    result = md.convert(r'SOURCE_FILE_PATH')
    content = result.text_content
    
    output = Path(r'OUTPUT_MD_PATH')
    output.write_text(content, encoding='utf-8')
    print(f'转换成功：{output}')
    print(f'内容长度：{len(content)} 字符')
    
    # 扫描版PDF检测：内容过于稀少则给出提示
    if r'SOURCE_FILE_PATH'.lower().endswith('.pdf') and len(content.strip()) < 200:
        print('提示：PDF内容极少，可能是扫描版。如需OCR识别，请将PDF各页截图后逐张转换。')
except Exception as e:
    print(f'错误: {e}', file=sys.stderr)
    sys.exit(1)
"@
```

---

### 第四步：报告结果

转换完成后告知用户：
- 输出文件完整路径
- 识别/转换的字符数
- 若字符数 < 100，提示效果可能不佳

---

## 多文件批量转换

如果用户提供多个文件路径（逗号或换行分隔），逐一执行上述流程，最后汇总：

```
转换完成：
  ✓ file1.png → file1.md（387字符，RapidOCR）
  ✓ file2.docx → file2.md（2341字符，markitdown）
  ✗ file3.pdf → 失败：[错误信息]
```

---

## 特殊情况处理

**音频文件需要 API Key：**
如转换 .mp3/.wav 时报错，告知用户：
```
音频转录需要 OpenAI API Key。
请设置环境变量 OPENAI_API_KEY 后重试。
```

**RapidOCR 首次运行下载模型：**
RapidOCR 首次运行会自动下载模型文件（约 20MB），需要网络连接，之后完全离线。如下载失败，检查网络后重试。
