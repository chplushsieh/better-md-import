#!/usr/bin/env python3
import argparse
import os
import re
from typing import List


# Matches Paper-style checkboxes: "[ ] task" or "[x] task" (with optional indentation)
# Group 1: leading whitespace (indentation)
# Group 2: checkbox state (x, X, or space)
# Group 3: the task text after the checkbox
# Examples: "[ ] buy milk", "    [x] done task", "[X] completed"
CHECKBOX_PAPER_RE = re.compile(r"^(\s*)\[\s*([xX ])\s*\]\s+(.*)$")

# Matches lines that are already Notion-style list checkboxes: "- [ ] task" or "- [x] task"
# Used to avoid double-converting lines that are already in the correct format
# Examples: "- [ ] todo item", "    - [x] completed item"
CHECKBOX_ALREADY_LIST_RE = re.compile(r"^(\s*)-\s*\[\s*[xX ]\s*\]\s+.*$")

# Matches quote lines: "> quote text" (with optional indentation and optional space after >)
# Group 1: leading whitespace (indentation)
# Examples: "> this is a quote", "    > nested quote", ">no space after angle"
QUOTE_RE = re.compile(r"^(\s*)>\s?.*$")


def convert_paper_to_notion_markdown(lines: List[str],
    line_break_trick_enabled: bool) -> List[str]:
    converted: List[str] = []
    i = 0
    total = len(lines)

    while i < total:
        line = lines[i].rstrip("\n")

        # 1) Convert Paper-style checkbox to Notion-style list checkbox
        # Paper: "[ ] task" or "[x] task" (optionally indented)
        # Notion: "- [ ]  task" with two spaces after ]
        if not CHECKBOX_ALREADY_LIST_RE.match(line):
            m = CHECKBOX_PAPER_RE.match(line)
            if m:
                indent, mark, text = m.groups()
                mark_lower = "x" if mark.lower() == "x" else " "
                converted.append(f"{indent}- [{mark_lower}]  {text}")
                i += 1
                continue

        # 2) Ensure quote line is preceded by and followed by an empty line
        # If we see a quote line and the previous/next line is not blank and not quoted, insert
        # an extra empty line before/after the quote line
        qm = QUOTE_RE.match(line)
        if qm:
            indent = qm.group(1)

            # Check if we need to add an empty line before this quote
            need_empty_before = False
            if i > 0:
                prev_line = lines[i - 1].rstrip("\n")
                # Need empty line if previous line is not empty and not a quote
                if prev_line.strip() != "" and not QUOTE_RE.match(prev_line):
                    need_empty_before = True
            
            # Check if we need to add an empty line after this quote
            need_empty_after = False
            if i + 1 < total:
                next_line = lines[i + 1].rstrip("\n")
                # Need empty line if next line is not empty and not a quote
                if next_line.strip() != "" and not QUOTE_RE.match(next_line):
                    need_empty_after = True
            
            # Add empty line before if needed
            if need_empty_before:
                converted.append("")
            
            # Add the quote line
            converted.append(line)
            
            # Add empty line after if needed
            if need_empty_after:
                converted.append("")
            
            i += 1
            continue

        # If the line is empty, insert a new line of a rare character before it
        if line == "" and line_break_trick_enabled:
            
            # Check if this is the case:
            need_special_char = True
            need_indent = 0
            if i > 0 and i + 1 < total:
                prev_line = lines[i - 1].rstrip("\n")
                next_line = lines[i + 1].rstrip("\n")
                # get indent of both previous and next line
                prev_indent = len(prev_line) - len(prev_line.lstrip())
                next_indent = len(next_line) - len(next_line.lstrip())
                need_indent = max(prev_indent, next_indent)

                # if one of the neighboring lines is a quote, then 
                # we don't need to insert a special character
                if QUOTE_RE.match(prev_line) or QUOTE_RE.match(next_line):
                    need_special_char = False
                
                # If both the previous line and the next line are empty or quoted, then
                # we don't need to insert any new lines.
                if (prev_line.strip() == "" or QUOTE_RE.match(prev_line)) and \
                (next_line.strip() == "" or QUOTE_RE.match(next_line)):
                    need_special_char = False
            
            if need_special_char:
                converted.append(" "*need_indent + "␣")
        
        # Default: pass through unchanged
        converted.append(line)
        
        i += 1

    # Re-append newlines
    return [l + "\n" for l in converted]


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Dropbox Paper Markdown to Notion-friendly Markdown.")
    parser.add_argument("input_path", help="Path to the input Markdown file from Paper")
    parser.add_argument("output_dir", help="Directory to write the converted Markdown file")
    parser.add_argument("--line-break-trick", action="store_true", 
        default=False,
        help="Enable line break trick. This will insert a rare character at the beginning of each empty line.")
    args = parser.parse_args()

    input_path = os.path.abspath(args.input_path)
    output_dir = os.path.abspath(args.output_dir)

    if not os.path.isfile(input_path):
        raise SystemExit(f"Input file not found: {input_path}")

    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    converted_lines = convert_paper_to_notion_markdown(lines, 
        line_break_trick_enabled=args.line_break_trick)

    # Notes exported from Dropbox Paper have an underscore in the filename
    # Replace underscores with spaces in the filename
    output_filename = os.path.basename(input_path).replace("_", " ")
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.writelines(converted_lines)

    print(f"Converted file written to: {output_path}")


if __name__ == "__main__":
    main()


