#!/usr/bin/env python3
"""
Fix folder name mismatches between chapterwithsummaryfromfile and inputstory calls.
Update chapterwithsummaryfromfile to use the indexed folder names that inputstory uses.
"""

import re
import pandas as pd

def read_chapters_data():
    """Read the chapters analysis CSV file."""
    df = pd.read_csv('utils/chapters_analysis.csv')
    return df

def create_folder_mapping(df):
    """Create mapping from old folder names to indexed folder names."""
    mapping = {}
    
    for _, row in df.iterrows():
        old_folder_name = row['chapter_title']  # BanachTarskiParadox
        indexed_folder_name = row['file_path']  # 01_BanachTarskiParadox
        
        # Map old name to new name
        mapping[old_folder_name] = indexed_folder_name
    
    return mapping

def fix_main_tex():
    """Fix the chapterwithsummaryfromfile calls in main.tex."""
    
    # Read chapters data
    df = read_chapters_data()
    folder_mapping = create_folder_mapping(df)
    
    # Read main.tex
    with open('main.tex', 'r') as f:
        content = f.read()
    
    # Find and replace chapterwithsummaryfromfile calls
    pattern = r'\\chapterwithsummaryfromfile\[([^\]]+)\]\{([^}]+)\}'
    
    def replace_folder(match):
        label = match.group(1)
        old_folder = match.group(2)
        
        if old_folder in folder_mapping:
            new_folder = folder_mapping[old_folder]
            print(f"Updating: {old_folder} → {new_folder}")
            return f'\\chapterwithsummaryfromfile[{label}]{{{new_folder}}}'
        else:
            print(f"Warning: No mapping found for {old_folder}")
            return match.group(0)
    
    # Apply replacements
    new_content = re.sub(pattern, replace_folder, content)
    
    # Count changes
    original_matches = re.findall(pattern, content)
    new_matches = re.findall(pattern, new_content)
    
    print(f"\nProcessed {len(original_matches)} chapterwithsummaryfromfile calls")
    
    # Write back to file
    with open('main.tex', 'w') as f:
        f.write(new_content)
    
    print("✅ Updated main.tex with indexed folder names")

if __name__ == "__main__":
    fix_main_tex() 