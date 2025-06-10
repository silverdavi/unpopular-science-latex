#!/usr/bin/env python3

import re

def fix_underscore_errors(filename):
    """Fix underscore errors in \ifdefined commands"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace underscores in \ifdefined\show_ commands with \textunderscore{}
    # Pattern: \ifdefined\show_XX_YYY
    pattern = r'\\ifdefined\\show_(\d+)_([^}\s]+)'
    
    def replace_func(match):
        number = match.group(1)
        name = match.group(2)
        return f'\\ifdefined\\show{{{number}textunderscore{{{name}}}}}'
    
    # Actually, let's use a simpler approach - protect the whole thing
    content = re.sub(r'\\ifdefined\\show_(\d+_[^}\s\n]+)', 
                     r'\\ifdefined\\protect\\show\textunderscore{}\1', 
                     content)
    
    # Even simpler - just escape underscores in these contexts
    content = re.sub(r'\\ifdefined\\show_', r'\\ifdefined\\show\\_', content)
    
    # Create backup
    with open(filename + '.backup3', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Write fixed version
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed underscore errors in {filename}")
    print(f"Backup saved as {filename}.backup3")

if __name__ == "__main__":
    fix_underscore_errors("main.tex") 