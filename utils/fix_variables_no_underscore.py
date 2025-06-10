#!/usr/bin/env python3

import re

def fix_variables_no_underscore(filename):
    """Replace show_XX_Name variables with showXXName format"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup
    with open(filename + '.backup4', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Fix \def statements: \def\show_01_BanachTarskiParadox{} -> \def\show01BanachTarskiParadox{}
    content = re.sub(r'\\def\\show_(\d+)_([^{}]+)\{\}', r'\\def\\show\1\2{}', content)
    
    # Fix \ifdefined statements: \ifdefined\show_01_BanachTarskiParadox -> \ifdefined\show01BanachTarskiParadox
    content = re.sub(r'\\ifdefined\\show_(\d+)_([^\s\n]+)', r'\\ifdefined\\show\1\2', content)
    
    # Write fixed version
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed variables to remove underscores in {filename}")
    print(f"Backup saved as {filename}.backup4")

if __name__ == "__main__":
    fix_variables_no_underscore("main.tex") 