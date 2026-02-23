# ImgTool

Privacy-first local image utility for resize, convert, batch processing, and optional OCR.

## Install (CLI App with pipx)

```bash
pipx install "$HOME/Desktop/projects/imgtool[gui,ocr]"
```

Use an absolute path to your local checkout.  
Example check:

```bash
imgtool -h
```

Notes:
- `pipx install <path>` installs only base dependencies unless extras are included in the path spec.
- OCR is pinned to a `textract` version compatible with modern `pipx` dependency parsing.

## Install (Development with Poetry)

```bash
poetry install
poetry install --extras "gui"
poetry install --extras "ocr"
poetry install --all-extras
```

## Commands

```bash
imgtool resize input.jpg --width 1200 --fit contain
imgtool batch-resize ./images --width 1200 --recursive --out ./processed
imgtool convert input.png --format webp
imgtool extract-text input.jpg --engine textract --ocr-format txt
imgtool gui
```

## Commands (Development)

```bash
poetry run imgtool resize input.jpg --width 1200 --fit contain
poetry run imgtool batch-resize ./images --width 1200 --recursive --out ./processed
poetry run imgtool convert input.png --format webp
poetry run imgtool extract-text input.jpg --engine textract --ocr-format txt
poetry run imgtool gui
```

## Help

```bash
imgtool -h
imgtool resize -h

# If running in development:
poetry run imgtool -h
poetry run imgtool resize -h
```
