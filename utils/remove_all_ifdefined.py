#!/usr/bin/env python3
"""
Remove all \ifdefined blocks from main.tex, keeping only the chapter content inside.
This will make all chapters unconditionally included.
"""

import re

def remove_ifdefined_blocks(content):
    """
    Remove \ifdefined...\fi blocks, keeping the content inside.
    
    Pattern matches:
    \ifdefined\ch##show...
    \chapterwithsummaryfromfile[...]{...}
    \inputstory{...}
    \fi
    """
    
    # Pattern to match entire ifdefined blocks
    # This captures the content between \ifdefined and \fi
    pattern = r'\\ifdefined\\ch\d+show\w+\s*\n(.*?)\n\\fi'
    
    def replacement(match):
        # Return just the content inside the block (group 1)
        content_inside = match.group(1)
        return content_inside
    
    # Apply the replacement with DOTALL flag to match across multiple lines
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    return updated_content

def main():
    # Read main.tex
    with open('main.tex', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Original content length:", len(content))
    
    # Count original ifdefined blocks
    original_count = len(re.findall(r'\\ifdefined\\ch\d+show\w+', content))
    print(f"Found {original_count} \\ifdefined blocks")
    
    # Remove all ifdefined blocks
    updated_content = remove_ifdefined_blocks(content)
    
    print("Updated content length:", len(updated_content))
    
    # Verify all ifdefined blocks are gone
    remaining_count = len(re.findall(r'\\ifdefined\\ch\d+show\w+', updated_content))
    print(f"Remaining \\ifdefined blocks: {remaining_count}")
    
    # Save the updated content
    with open('main.tex', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Successfully removed {original_count} \\ifdefined blocks!")
    print("All chapters are now unconditionally included.")

if __name__ == "__main__":
    main() 