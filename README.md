# 📧 EML to MBOX Converter

![Python](https://img.shields.io/badge/python-3.x-blue)
![Platform](https://img.shields.io/badge/platform-macOS%20|%20Linux%20|%20Windows-lightgrey)

Convert `.eml` files into `.mbox` format. Works with exports from Outlook, Thunderbird, MailStore and other email clients.

## ✨ Features

- **Batch Conversion**: Convert entire directories of `.eml` files to a single `.mbox` file.
- **Encoding Safe**: Preserves original encoding (UTF-8, ISO-8859-*, KOI8-R, etc.) so emails in any language stay intact.
- **Recursive Support**: Process `.eml` files in subdirectories with `-r`.
- **Deduplication**: Skip repeated messages by `Message-ID` with `-d` / `--dedupe`. Handy for incremental backups.
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

# Include subdirectories and skip duplicate messages
python3 eml_to_mbox.py -r -d /path/to/eml_folder /path/to/output.mbox
```

## 🧹 Deduplication

With `-d` / `--dedupe`, each message's `Message-ID` header is checked and only the **first occurrence** is written. Files are processed in sorted path order, so "first" means the first matching file by path. Messages that have no `Message-ID` header are always kept, and the summary line tells you how many duplicates were skipped.

Note that `.eml` files don't record which mail folder a message came from, so the `.mbox` output doesn't either.

## 🪟 Windows

```shell
python eml_to_mbox.py C:\path\to\emls C:\path\to\output.mbox
```

## ⚠️ Caution

This tool does **not** modify or delete your original `.eml` files. However, the conversion may not be perfect for every email. Always keep your original files until you have verified the output is correct and complete.

## 📄 License

[MIT](LICENSE)
