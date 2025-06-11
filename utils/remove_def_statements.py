#!/usr/bin/env python3
"""
Remove all \def statements for chapter variables from main.tex.
Since we removed all \ifdefined blocks, these \def statements are no longer needed.
"""

import re

def remove_def_statements(content):
    """
    Remove all \def statements for chapter variables.
    
    Patterns to remove:
    \def\ch##show...{}
    %\def\ch##show...{}  (commented ones too)
    """
    
    # Remove active \def statements
    content = re.sub(r'\\def\\ch\d+show\w+\{\}\s*\n?', '', content)
    
    # Remove commented \def statements
    content = re.sub(r'%\\def\\ch\d+show\w+\{\}\s*\n?', '', content)
    
    return content

def main():
    # Read main.tex
    with open('main.tex', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Original content length:", len(content))
    
    # Count original def statements
    active_count = len(re.findall(r'\\def\\ch\d+show\w+', content))
    commented_count = len(re.findall(r'%\\def\\ch\d+show\w+', content))
    total_count = active_count + commented_count
    print(f"Found {active_count} active \\def statements")
    print(f"Found {commented_count} commented \\def statements")
    print(f"Total: {total_count} \\def statements")
    
    # Remove all def statements
    updated_content = remove_def_statements(content)
    
    print("Updated content length:", len(updated_content))
    
    # Verify all def statements are gone
    remaining_active = len(re.findall(r'\\def\\ch\d+show\w+', updated_content))
    remaining_commented = len(re.findall(r'%\\def\\ch\d+show\w+', updated_content))
    remaining_total = remaining_active + remaining_commented
    print(f"Remaining \\def statements: {remaining_total}")
    
    # Save the updated content
    with open('main.tex', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Successfully removed {total_count} \\def statements!")
    print("Chapter variables are no longer needed.")

if __name__ == "__main__":
    main() 