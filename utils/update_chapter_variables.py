#!/usr/bin/env python3
"""
Update chapter variable names in main.tex from showChapterName to ch##showChapterName format
using the chapters_analysis.csv file to get the proper mapping.
"""

import pandas as pd
import re
import os

def read_chapters_data():
    """Read the chapters analysis CSV file."""
    csv_path = 'utils/chapters_analysis.csv'
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Could not find {csv_path}")
    
    df = pd.read_csv(csv_path)
    return df

def create_variable_mapping(df):
    """Create mapping from old variable names to new format."""
    mapping = {}
    
    for _, row in df.iterrows():
        order = row['order']
        ifdefined_name = row['ifdefined_name']
        
        # Extract the chapter name from ifdefined_name (remove show_ prefix and number prefix)
        # e.g., show_01_BanachTarskiParadox -> BanachTarskiParadox
        if ifdefined_name.startswith('show_'):
            # Remove 'show_' and the number prefix (e.g., '01_')
            chapter_name = re.sub(r'^show_\d+_', '', ifdefined_name)
            old_var = f'show{chapter_name}'
            new_var = f'ch{order:02d}show{chapter_name}'
            mapping[old_var] = new_var
    
    return mapping

def update_main_tex(mapping):
    """Update main.tex with new variable names."""
    main_tex_path = 'main.tex'
    
    if not os.path.exists(main_tex_path):
        raise FileNotFoundError(f"Could not find {main_tex_path}")
    
    # Read the file
    with open(main_tex_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Keep track of changes
    changes_made = []
    
    # Update \def statements (both commented and uncommented)
    for old_var, new_var in mapping.items():
        # Pattern for \def statements
        def_pattern = rf'\\def\\{re.escape(old_var)}\{{\}}'
        def_replacement = rf'\\def\\{new_var}{{}}'
        
        # Count matches before replacement
        matches = re.findall(def_pattern, content)
        if matches:
            content = re.sub(def_pattern, def_replacement, content)
            changes_made.append(f"Updated \\def\\{old_var}{{}} -> \\def\\{new_var}{{}}")
    
    # Update \ifdefined statements
    for old_var, new_var in mapping.items():
        # Pattern for \ifdefined statements
        ifdefined_pattern = rf'\\ifdefined\\{re.escape(old_var)}'
        ifdefined_replacement = rf'\\ifdefined\\{new_var}'
        
        # Count matches before replacement
        matches = re.findall(ifdefined_pattern, content)
        if matches:
            content = re.sub(ifdefined_pattern, ifdefined_replacement, content)
            changes_made.append(f"Updated \\ifdefined\\{old_var} -> \\ifdefined\\{new_var}")
    
    # Write the updated content back
    with open(main_tex_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return changes_made

def main():
    """Main function to update chapter variables."""
    print("Reading chapters analysis data...")
    df = read_chapters_data()
    print(f"Found {len(df)} chapters in CSV")
    
    print("Creating variable mapping...")
    mapping = create_variable_mapping(df)
    print(f"Created {len(mapping)} variable mappings")
    
    # Show some examples of the mapping
    print("\nExample mappings:")
    for i, (old_var, new_var) in enumerate(list(mapping.items())[:5]):
        print(f"  {old_var} -> {new_var}")
    if len(mapping) > 5:
        print(f"  ... and {len(mapping) - 5} more")
    
    print("\nUpdating main.tex...")
    changes = update_main_tex(mapping)
    
    print(f"\nCompleted! Made {len(changes)} changes:")
    for change in changes[:10]:  # Show first 10 changes
        print(f"  {change}")
    if len(changes) > 10:
        print(f"  ... and {len(changes) - 10} more changes")

if __name__ == "__main__":
    main() 