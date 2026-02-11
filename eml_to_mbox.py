#!/usr/bin/env python3
import os
import re
import time
import email.utils

_UTF8_BOM = b'\xef\xbb\xbf'

_FROM_LINE_RE = re.compile(rb'^(>*From )', re.MULTILINE)
_HEADER_FROM_RE = re.compile(
    r'^From:\s*(.*(?:\n[ \t]+.*)*)', re.MULTILINE | re.IGNORECASE
)
_HEADER_RETURNPATH_RE = re.compile(
    r'^Return-Path:\s*<?([^>\s]+)>?', re.MULTILINE | re.IGNORECASE
)
_HEADER_DATE_RE = re.compile(
    r'^Date:\s*(.*)', re.MULTILINE | re.IGNORECASE
)
_EMAIL_ADDR_ANGLE_RE = re.compile(r'<([^>]+)>')
_EMAIL_ADDR_BARE_RE = re.compile(r'[\w.\-+]+@[\w.\-]+')


def _find_header_boundary(raw_bytes):
    pos = raw_bytes.find(b'\r\n\r\n')
    if pos == -1:
        pos = raw_bytes.find(b'\n\n')
    return pos if pos != -1 else len(raw_bytes)


def _get_headers_text(raw_bytes):
    end = _find_header_boundary(raw_bytes)
    try:
        return raw_bytes[:end].decode('ascii', errors='replace'), end
    except Exception:
        return '', end


def _extract_from_address(headers_text):
    match = _HEADER_FROM_RE.search(headers_text)
    if match:
        from_value = match.group(1).replace('\n', ' ').strip()
        addr_match = _EMAIL_ADDR_ANGLE_RE.search(from_value)
        if addr_match:
            return addr_match.group(1)
        addr_match = _EMAIL_ADDR_BARE_RE.search(from_value)
        if addr_match:
            return addr_match.group(0)

    match = _HEADER_RETURNPATH_RE.search(headers_text)
    if match:
        return match.group(1)

    return 'unknown'


def _extract_date(headers_text):
    match = _HEADER_DATE_RE.search(headers_text)
    if match:
        try:
            parsed = email.utils.parsedate(match.group(1).strip())
            if parsed:
                return time.asctime(parsed)
        except Exception:
            pass
    return time.asctime()


def _strip_existing_envelope(raw_bytes):
    if raw_bytes.startswith(b'From ') and not raw_bytes.startswith(b'From:'):
        first_newline = raw_bytes.find(b'\n')
        if first_newline != -1:
            first_line = raw_bytes[:first_newline]
            if b'@' in first_line or b'MAILER-DAEMON' in first_line:
                return raw_bytes[first_newline + 1:]
    return raw_bytes


def _collect_eml_files(folder, recursive=False):
    eml_files = []
    if recursive:
        for dirpath, _dirnames, filenames in os.walk(folder):
            for fn in filenames:
                if fn.lower().endswith('.eml'):
                    eml_files.append(os.path.join(dirpath, fn))
        eml_files.sort()
    else:
        eml_files = sorted([
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith('.eml')
        ])
    return eml_files


def convert_eml_to_mbox(eml_folder, mbox_file, recursive=False):
    """
    Convert .eml files to a single .mbox file using raw byte writes
    to preserve original encoding. Uses mboxrd quoting.
    """
    eml_files = _collect_eml_files(eml_folder, recursive)

    if not eml_files:
        print(f"No .eml files found in {eml_folder}")
        return

    converted = 0
    failed = 0

    with open(mbox_file, 'wb') as mbox:
        for eml_path in eml_files:
            eml_file = os.path.basename(eml_path)
            try:
                with open(eml_path, 'rb') as f:
                    raw = f.read()

                if raw.startswith(_UTF8_BOM):
                    raw = raw[len(_UTF8_BOM):]

                raw = _strip_existing_envelope(raw)

                if len(raw.strip()) == 0:
                    print(f"Warning: Skipping empty file {eml_file}")
                    failed += 1
                    continue

                headers_text, _ = _get_headers_text(raw)
                sender = _extract_from_address(headers_text)
                date_str = _extract_date(headers_text)

                envelope = f"From {sender} {date_str}\n".encode(
                    'ascii', errors='replace'
                )
                mbox.write(envelope)

                content = raw.replace(b'\r\n', b'\n')
                content = _FROM_LINE_RE.sub(rb'>\1', content)

                mbox.write(content)

                if not content.endswith(b'\n'):
                    mbox.write(b'\n\n')
                elif not content.endswith(b'\n\n'):
                    mbox.write(b'\n')

                converted += 1

            except Exception as e:
                print(f"Warning: Failed to convert {eml_file}: {e}")
                failed += 1

    print(f"Conversion complete! {converted} email(s) saved to {mbox_file}", end="")
    if failed:
        print(f" ({failed} failed)")
    else:
        print()


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        prog="eml_to_mbox",
        description=(
            "Convert .eml files exported from Outlook, Thunderbird, MailStore "
            "or other email clients into a single .mbox file.\n\n"
            "Preserves original encoding of all message parts (UTF-8, "
            "ISO-8859-*, KOI8-R, etc.) so emails in any language are "
            "kept intact without garbling."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  %(prog)s ./my_emails output.mbox\n"
            "  %(prog)s C:\\ExportedMail\\Inbox emails.mbox\n"
            "  %(prog)s /home/user/eml_backup combined.mbox\n"
            "\n"
            "The output .mbox file can be imported into Thunderbird, Apple\n"
            "Mail, mutt, or any other email client that supports mbox format.\n"
            "\n"
            "CAUTION: This tool does NOT modify or delete your original .eml\n"
            "files. However, the conversion process may not be perfect for\n"
            "every email. Always keep your original .eml files until you have\n"
            "verified that the output .mbox file is correct and complete."
        ),
    )
    parser.add_argument(
        "eml_folder",
        metavar="EML_FOLDER",
        help="path to the folder containing .eml files",
    )
    parser.add_argument(
        "mbox_file",
        metavar="OUTPUT_MBOX",
        help="path for the output .mbox file (will be created/overwritten)",
    )
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="also process .eml files in subdirectories",
    )

    args = parser.parse_args()

    # --- Validate inputs ---
    if not os.path.exists(args.eml_folder):
        print(f"Error: Folder not found: '{args.eml_folder}'")
        print("  Make sure the path exists and is spelled correctly.")
        sys.exit(1)

    if not os.path.isdir(args.eml_folder):
        print(f"Error: '{args.eml_folder}' is not a directory.")
        print("  The first argument must be a folder containing .eml files.")
        sys.exit(1)

    eml_count = sum(
        1 for f in _collect_eml_files(args.eml_folder, args.recursive)
    )
    if eml_count == 0:
        print(f"Error: No .eml files found in '{args.eml_folder}'")
        print("  Make sure the folder contains files with a .eml extension.")
        sys.exit(1)

    # Check output directory is writable
    output_dir = os.path.dirname(os.path.abspath(args.mbox_file))
    if not os.path.isdir(output_dir):
        print(f"Error: Output directory does not exist: '{output_dir}'")
        print("  Create the directory first, or choose a different output path.")
        sys.exit(1)

    if os.path.exists(args.mbox_file) and not os.access(args.mbox_file, os.W_OK):
        print(f"Error: Cannot write to '{args.mbox_file}' (permission denied).")
        sys.exit(1)

    print(f"Found {eml_count} .eml file(s) in '{args.eml_folder}'")
    print(f"Converting to '{args.mbox_file}'...")
    print()

    convert_eml_to_mbox(args.eml_folder, args.mbox_file, args.recursive)
