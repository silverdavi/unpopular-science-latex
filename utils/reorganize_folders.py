#!/usr/bin/env python3
"""
Folder Reorganization Script
1. Remove folders not in the 53 chapters list
2. Rename folders to include index prefix (01_, 02_, etc.)
3. Update main.tex accordingly
"""

import pandas as pd
import shutil
import os
from pathlib import Path
import re


def get_chapter_folders():
    """Get the list of 53 folders from CSV"""
    df = pd.read_csv('utils/chapters_analysis.csv')
    return df[['order', 'file_path']].to_dict('records')


def get_existing_folders():
    """Get list of existing directories (excluding special ones)"""
    exclude_dirs = {'utils', 'venv', 'cover', '.git'}
    existing = []
    
    for item in os.listdir('.'):
        if os.path.isdir(item) and item not in exclude_dirs and not item.startswith('.'):
            existing.append(item)
    
    return existing


def main():
    print("📁 Starting folder reorganization...")
    
    # Get chapter data
    chapters = get_chapter_folders()
    chapter_folders = {ch['file_path']: ch['order'] for ch in chapters}
    
    # Get existing folders
    existing_folders = get_existing_folders()
    
    print(f"Found {len(existing_folders)} existing folders")
    print(f"Need to keep {len(chapters)} chapter folders")
    
    # Identify folders to remove
    folders_to_remove = []
    folders_to_rename = []
    
    for folder in existing_folders:
        if folder in chapter_folders:
            folders_to_rename.append((folder, chapter_folders[folder]))
        else:
            folders_to_remove.append(folder)
    
    print(f"\n🗑️  Folders to remove ({len(folders_to_remove)}):")
    for folder in folders_to_remove:
        print(f"  - {folder}")
    
    print(f"\n🔄 Folders to rename ({len(folders_to_rename)}):")
    rename_mapping = {}
    for old_name, order in folders_to_rename:
        new_name = f"{order:02d}_{old_name}"
        rename_mapping[old_name] = new_name
        print(f"  - {old_name} → {new_name}")
    
    # Ask for confirmation
    response = input(f"\n⚠️  This will remove {len(folders_to_remove)} folders and rename {len(folders_to_rename)} folders. Continue? [y/N]: ")
    
    if response.lower() != 'y':
        print("❌ Operation cancelled.")
        return
    
    # Remove irrelevant folders
    print(f"\n🗑️  Removing {len(folders_to_remove)} folders...")
    for folder in folders_to_remove:
        try:
            shutil.rmtree(folder)
            print(f"  ✅ Removed: {folder}")
        except Exception as e:
            print(f"  ❌ Error removing {folder}: {e}")
    
    # Rename chapter folders
    print(f"\n🔄 Renaming {len(folders_to_rename)} folders...")
    successful_renames = {}
    
    for old_name, order in folders_to_rename:
        new_name = f"{order:02d}_{old_name}"
        try:
            os.rename(old_name, new_name)
            successful_renames[old_name] = new_name
            print(f"  ✅ Renamed: {old_name} → {new_name}")
        except Exception as e:
            print(f"  ❌ Error renaming {old_name}: {e}")
    
    # Update main.tex
    print(f"\n📝 Updating main.tex...")
    update_main_tex(successful_renames)
    
    print(f"\n🎉 Reorganization complete!")
    print(f"  - Removed: {len(folders_to_remove)} folders")
    print(f"  - Renamed: {len(successful_renames)} folders")
    print(f"  - Updated: main.tex")


def update_main_tex(rename_mapping):
    """Update main.tex file with new folder names"""
    
    # Read main.tex
    with open('main.tex', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup
    with open('main.tex.backup', 'w', encoding='utf-8') as f:
        f.write(content)
    print("  📋 Created backup: main.tex.backup")
    
    # Update inputstory references
    updates_made = 0
    for old_name, new_name in rename_mapping.items():
        # Pattern to match \inputstory{old_name}
        old_pattern = f'\\inputstory{{{old_name}}}'
        new_pattern = f'\\inputstory{{{new_name}}}'
        
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            updates_made += 1
            print(f"  ✅ Updated reference: {old_name} → {new_name}")
    
    # Write updated content
    with open('main.tex', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  📝 Made {updates_made} updates to main.tex")


if __name__ == "__main__":
    main() 