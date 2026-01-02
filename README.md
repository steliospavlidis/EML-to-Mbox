# 📧 EML to MBOX Converter

![Python](https://img.shields.io/badge/python-3.x-blue)
![Platform](https://img.shields.io/badge/platform-macOS%20|%20Linux%20|%20Windows-lightgrey)

Seamlessly convert your `.eml` files into the universally accepted `.mbox` format with this lightweight, efficient, and user-friendly command-line tool. Whether you're migrating emails, archiving them, or just need a unified format, **EML to MBOX Converter** has got you covered.

## ✨ Features

- **Batch Conversion**: Effortlessly convert entire directories of `.eml` files to a single `.mbox` file.
- **Cross-Platform Compatibility**: Works flawlessly on macOS, Linux, and Windows.
- **Zero Dependencies**: Leverages Python’s built-in libraries—no need for additional installations.
- **Customizable & Extensible**: The code is clean, well-documented, and easily adaptable to your specific needs.
- **Performance-Optimized**: Handles large volumes of email data with ease.

## 🚀 Quick Start

```bash
# 1. Clone the Repository
git clone https://github.com/steliospavlidis/EML-to-Mbox.git
cd eml-to-mbox-converter

# 2. Run the Script
python3 eml_to_mbox.py /path/to/eml_folder /path/to/output.mbox

# 3. (Optional) Make Executable on Unix Systems
chmod +x eml_to_mbox.py
./eml_to_mbox.py /path/to/eml_folder /path/to/output.mbox
```

## 🪟 Windows Notes

On Windows, always invoke the script explicitly via Python:

```shell
python eml_to_mbox.py C:\path\to\emls C:\path\to\output.mbox
```
