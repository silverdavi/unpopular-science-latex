#!/usr/bin/env python3
"""
Fix Em Dashes in TeX Files
==========================
Replaces non-padded em dashes "—" with padded em dashes " — " in all .tex files.

This script:
1. Recursively finds all .tex files
2. Replaces em dashes that lack proper spacing
3. Preserves already properly spaced em dashes
4. Shows progress and statistics
"""

import os
import re
from pathlib import Path

def fix_em_dashes_in_text(text):
    """
    Replace non-padded em dashes with padded ones.
    
    Patterns handled:
    - "word—word" → "word — word"
    - " —word" → " — word" 
    - "word— " → "word — "
    - "—word" (start of line) → "— word"
    - "word—" (end of line) → "word —"
    
    Preserves already correct: " — "
    """
    original_text = text
    
    # Pattern 1: Em dash with no space before OR after (but not both missing)
    # This handles cases like "word—word", "word— ", " —word"
    text = re.sub(r'(\S)—(\S)', r'\1 — \2', text)  # word—word → word — word
    text = re.sub(r'(\S)— ', r'\1 — ', text)       # word— → word — 
    text = re.sub(r' —(\S)', r' — \1', text)       # —word → — word
    
    # Pattern 2: Em dash at start of line with no space after
    text = re.sub(r'^—(\S)', r'— \1', text, flags=re.MULTILINE)  # —word → — word
    
    # Pattern 3: Em dash at end of line with no space before  
    text = re.sub(r'(\S)—$', r'\1 —', text, flags=re.MULTILINE)  # word— → word —
    
    return text

def process_tex_files():
    """Process all .tex files in the current directory and subdirectories."""
    
    # Find all .tex files
    tex_files = list(Path('.').rglob('*.tex'))
    
    if not tex_files:
        print("❌ No .tex files found in current directory")
        return
    
    print(f"🔍 Found {len(tex_files)} .tex files")
    print("📝 Processing em dashes...")
    print("=" * 60)
    
    total_replacements = 0
    files_modified = 0
    
    for tex_file in sorted(tex_files):
        try:
            # Read file
            with open(tex_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Fix em dashes
            fixed_content = fix_em_dashes_in_text(original_content)
            
            # Count changes
            if fixed_content != original_content:
                # Count number of em dashes that were changed
                original_em_count = original_content.count('—')
                fixed_em_count = fixed_content.count('—')
                
                # Simple heuristic: count how many positions changed
                changes = 0
                original_lines = original_content.split('\n')
                fixed_lines = fixed_content.split('\n')
                
                for orig_line, fixed_line in zip(original_lines, fixed_lines):
                    if orig_line != fixed_line:
                        # Count em dashes that gained spaces
                        changes += len(re.findall(r'\S—\S|^\S—|\S—$|\S— | —\S', orig_line))
                
                if changes > 0:
                    # Write back to file
                    with open(tex_file, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    
                    print(f"✅ {tex_file}: {changes} em dash(es) fixed")
                    total_replacements += changes
                    files_modified += 1
                
        except Exception as e:
            print(f"❌ Error processing {tex_file}: {e}")
    
    print("=" * 60)
    if total_replacements > 0:
        print(f"🎉 COMPLETED:")
        print(f"   📁 Files modified: {files_modified}")
        print(f"   🔧 Total em dashes fixed: {total_replacements}")
        print(f"   ✨ All em dashes now properly spaced: ' — '")
    else:
        print("✨ All em dashes were already properly spaced!")

def main():
    """Main execution function."""
    print("🚀 EM DASH FORMATTER FOR TEX FILES")
    print("=" * 60)
    print("Converting: '—' → ' — ' (adding proper spacing)")
    print("Preserving: ' — ' (already correct)")
    print()
    
    # Check if we're in the right directory
    if not Path('.').name.startswith('MainBook'):
        print("⚠️  Warning: Not in MainBook directory")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    process_tex_files()

if __name__ == "__main__":
    main() 