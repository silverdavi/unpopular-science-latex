#!/usr/bin/env python3
"""
Fix main.tex with renamed folders
"""

import pandas as pd

def main():
    # Get the rename mapping from CSV
    df = pd.read_csv('utils/chapters_analysis.csv')
    
    # Create mapping from old name to new name
    rename_mapping = {}
    for _, row in df.iterrows():
        old_name = row['file_path']
        new_name = f"{row['order']:02d}_{old_name}"
        rename_mapping[old_name] = new_name
    
    # Read main.tex
    with open('main.tex', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update inputstory references
    updates_made = 0
    for old_name, new_name in rename_mapping.items():
        old_pattern = f'\\inputstory{{{old_name}}}'
        new_pattern = f'\\inputstory{{{new_name}}}'
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            updates_made += 1
            print(f"✅ Updated: {old_name} → {new_name}")
    
    # Write updated content
    with open('main.tex', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n📝 Made {updates_made} updates to main.tex")

if __name__ == "__main__":
    main() 