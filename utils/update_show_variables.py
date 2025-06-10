#!/usr/bin/env python3
"""
Update show variable names in main.tex to include index prefixes
Changes showBanachTarskiParadox to show_01_BanachTarskiParadox
"""

import pandas as pd
import re

def main():
    print("🔄 Updating show variable names with index prefixes...")
    
    # Get the chapter data from CSV
    df = pd.read_csv('utils/chapters_analysis.csv')
    
    # Create mapping from old show variables to new ones
    show_mapping = {}
    for _, row in df.iterrows():
        old_show = row['ifdefined_name']  # e.g., showBanachTarskiParadox
        chapter_name = old_show.replace('show', '', 1)  # Remove 'show' prefix
        new_show = f"show_{row['order']:02d}_{chapter_name}"  # e.g., show_01_BanachTarskiParadox
        show_mapping[old_show] = new_show
    
    # Read main.tex
    with open('main.tex', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup
    with open('main.tex.backup2', 'w', encoding='utf-8') as f:
        f.write(content)
    print("📋 Created backup: main.tex.backup2")
    
    # Update \def statements
    def_updates = 0
    for old_show, new_show in show_mapping.items():
        old_def = f'\\def\\{old_show}{{}}'
        new_def = f'\\def\\{new_show}{{}}'
        
        if old_def in content:
            content = content.replace(old_def, new_def)
            def_updates += 1
            print(f"✅ Updated def: {old_show} → {new_show}")
    
    # Update \ifdefined statements
    ifdefined_updates = 0
    for old_show, new_show in show_mapping.items():
        old_ifdefined = f'\\ifdefined\\{old_show}'
        new_ifdefined = f'\\ifdefined\\{new_show}'
        
        if old_ifdefined in content:
            content = content.replace(old_ifdefined, new_ifdefined)
            ifdefined_updates += 1
            print(f"✅ Updated ifdefined: {old_show} → {new_show}")
    
    # Write updated content
    with open('main.tex', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n📝 Updates completed:")
    print(f"  - \\def statements: {def_updates}")
    print(f"  - \\ifdefined statements: {ifdefined_updates}")
    print(f"  - Total variables updated: {len(show_mapping)}")
    
    # Show a few examples of the mapping
    print(f"\n📋 Example mappings:")
    for i, (old, new) in enumerate(list(show_mapping.items())[:5]):
        print(f"  - {old} → {new}")
    if len(show_mapping) > 5:
        print(f"  ... and {len(show_mapping) - 5} more")

if __name__ == "__main__":
    main() 