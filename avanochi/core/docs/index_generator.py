import os
import re

def extract_headers_outside_code_blocks(text):
    # Remove all fenced code blocks (```...```)
    cleaned = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Extract headers from cleaned text
    return re.findall(r'^(#{1,6})\s+(.*)', cleaned, re.MULTILINE)

def generate_toc(readme_text):
    headers = extract_headers_outside_code_blocks(readme_text)
    toc_lines = []

    for hashes, title in headers:
        level = len(hashes)
        slug = title.strip().lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        link = f"[{title}](#{slug})"
        indent = '    ' * (level - 1)
        toc_lines.append(f"{indent}- {link}")

    # Append page break after TOC
    toc_lines.append('\n<div class="page-break"></div>\n')
    return '\n'.join(toc_lines)

def replace_toc(readme_text):
    pattern = r"(# Table of Contents\n\n)(.*?)(\n(?=#|\Z))"
    new_toc = generate_toc(readme_text)
    replacement = r"\1" + new_toc + r"\3"
    updated_readme = re.sub(pattern, replacement, readme_text, flags=re.DOTALL)
    return updated_readme

# Locate README.md in the same directory as the script
script_dir = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(script_dir, "README.md")

# Read, update, and overwrite README.md
with open(readme_path, "r", encoding="utf-8") as f:
    original_content = f.read()

updated_content = replace_toc(original_content)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(updated_content)
