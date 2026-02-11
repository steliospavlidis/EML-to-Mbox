# 📧 EML to MBOX Converter

![Python](https://img.shields.io/badge/python-3.x-blue)
![Platform](https://img.shields.io/badge/platform-macOS%20|%20Linux%20|%20Windows-lightgrey)

Convert `.eml` files into `.mbox` format. Works with exports from Outlook, Thunderbird, MailStore and other email clients.

## ✨ Features

- **Batch Conversion**: Convert entire directories of `.eml` files to a single `.mbox` file.
- **Encoding Safe**: Preserves original encoding (UTF-8, ISO-8859-*, KOI8-R, etc.) so emails in any language stay intact.
- **Recursive Support**: Process `.eml` files in subdirectories with `-r`.
- **Cross-Platform**: Works on macOS, Linux, and Windows.
- **Zero Dependencies**: Uses only Python built-in libraries.
- **Error Handling**: Clear error messages and per-file warnings.

## 🚀 Quick Start

```bash
git clone https://github.com/steliospavlidis/EML-to-Mbox.git
cd EML-to-Mbox

python3 eml_to_mbox.py /path/to/eml_folder /path/to/output.mbox

# Include subdirectories
python3 eml_to_mbox.py -r /path/to/eml_folder /path/to/output.mbox
```

## 🪟 Windows

```shell
python eml_to_mbox.py C:\path\to\emls C:\path\to\output.mbox
```

## ⚠️ Caution

This tool does **not** modify or delete your original `.eml` files. However, the conversion may not be perfect for every email. Always keep your original files until you have verified the output is correct and complete.
