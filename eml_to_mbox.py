#!/usr/bin/env python3
import os
import mailbox
from email import policy
from email.parser import BytesParser

def convert_eml_to_mbox(eml_folder, mbox_file):
    """
    Convert all .eml files in a folder to a single .mbox file.
    
    :param eml_folder: Path to the folder containing .eml files
    :param mbox_file: Path to the output .mbox file
    """
    # Create an mbox file
    mbox = mailbox.mbox(mbox_file)

    # Add each .eml file to the mbox
    for eml_file in os.listdir(eml_folder):
        eml_path = os.path.join(eml_folder, eml_file)
        if os.path.isfile(eml_path) and eml_file.endswith('.eml'):
            with open(eml_path, 'rb') as f:
                msg = BytesParser(policy=policy.default).parse(f)
                mbox.add(msg)

    # Close the mbox file
    mbox.close()
    print(f"Conversion complete! The mbox file is saved as {mbox_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert .eml files to .mbox format")
    parser.add_argument("eml_folder", help="Path to the folder containing .eml files")
    parser.add_argument("mbox_file", help="Path to the output .mbox file")

    args = parser.parse_args()

    convert_eml_to_mbox(args.eml_folder, args.mbox_file)
