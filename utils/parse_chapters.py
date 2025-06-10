#!/usr/bin/env python3
"""
Chapter Parser for LaTeX Book
Parses main.tex to extract chapter information and create a DataFrame
"""

import re
import pandas as pd
from pathlib import Path


def parse_tex_file(filepath):
    """Parse the main.tex file and extract chapter information"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chapters = []
    order = 0
    
    # Find all \def statements first to track which chapters are enabled
    enabled_chapters = set()
    def_pattern = r'\\def\\(show\w+)\{\}'
    for match in re.finditer(def_pattern, content):
        if not is_in_comment_block(content, match.start()):
            enabled_chapters.add(match.group(1))
    
    # Find all chapter definitions
    chapter_patterns = [
        # Pattern for \chapterwithsummaryfromfile
        r'\\ifdefined\\(show\w+)\s*\n\\chapterwithsummaryfromfile\[([^\]]+)\]\{([^}]+)\}\s*\n\\inputstory\{([^}]+)\}',
        # Pattern for \chapterwithsummary
        r'\\ifdefined\\(show\w+)\s*\n\\chapterwithsummary\[([^\]]+)\]\{([^}]+)\}\{[^}]*\}\s*\n\\inputstory\{([^}]+)\}',
        # Pattern for simple chapter
        r'\\ifdefined\\(show\w+)\s*\n\\chapter\[[^\]]*\]\{([^}]+)\}\s*\n\\label\{([^}]+)\}\s*\n\\inputstory\{([^}]+)\}'
    ]
    
    for pattern in chapter_patterns:
        for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
            if is_in_comment_block(content, match.start()):
                continue
                
            order += 1
            
            if len(match.groups()) == 4:
                # chapterwithsummaryfromfile or chapterwithsummary
                ifdefined_name = match.group(1)
                label = match.group(2)
                chapter_title = match.group(3)
                file_path = match.group(4)
            else:
                # simple chapter pattern would need different parsing
                continue
            
            is_enabled = ifdefined_name in enabled_chapters
            
            chapters.append({
                'order': order,
                'ifdefined_name': ifdefined_name,
                'chapter_title': chapter_title,
                'label': label,
                'file_path': file_path,
                'is_enabled': is_enabled,
                'status': 'ENABLED' if is_enabled else 'DISABLED'
            })
    
    return chapters


def is_in_comment_block(content, position):
    """Check if a position in the content is within a comment block"""
    
    # Find all comment blocks
    comment_blocks = []
    
    # Multi-line comments \begin{comment} ... \end{comment}
    for match in re.finditer(r'\\begin\{comment\}.*?\\end\{comment\}', content, re.DOTALL):
        comment_blocks.append((match.start(), match.end()))
    
    # Single line comments starting with %
    lines = content.split('\n')
    current_pos = 0
    for line in lines:
        line_start = current_pos
        line_end = current_pos + len(line)
        
        # Find % that's not escaped
        comment_start = -1
        for i, char in enumerate(line):
            if char == '%' and (i == 0 or line[i-1] != '\\'):
                comment_start = line_start + i
                break
        
        if comment_start != -1:
            comment_blocks.append((comment_start, line_end))
        
        current_pos = line_end + 1  # +1 for the newline character
    
    # Check if position is in any comment block
    for start, end in comment_blocks:
        if start <= position <= end:
            return True
    
    return False


def check_file_exists(file_path, possible_extensions=['.tex', '']):
    """Check if a file exists with possible extensions"""
    base_path = Path(file_path)
    
    # Check exact path first
    if base_path.exists():
        return True, str(base_path)
    
    # Try with extensions
    for ext in possible_extensions:
        full_path = base_path.with_suffix(ext)
        if full_path.exists():
            return True, str(full_path)
    
    return False, None


def extract_chapter_info_comprehensive(filepath):
    """More comprehensive extraction that handles various chapter formats"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chapters = []
    order = 0
    
    # Find enabled chapters
    enabled_chapters = set()
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('\\def\\show') and line.endswith('{}') and not line.startswith('%'):
            ifdefined_name = re.search(r'\\def\\(show\w+)\{\}', line)
            if ifdefined_name:
                enabled_chapters.add(ifdefined_name.group(1))
    
    # Find all ifdefined blocks
    ifdefined_pattern = r'\\ifdefined\\(show\w+)(.*?)\\fi'
    
    for match in re.finditer(ifdefined_pattern, content, re.DOTALL):
        if is_in_comment_block(content, match.start()):
            continue
            
        ifdefined_name = match.group(1)
        block_content = match.group(2)
        
        order += 1
        
        # Extract chapter information from the block
        chapter_title = "Unknown"
        label = "unknown"
        file_path = "unknown"
        chapter_type = "unknown"
        
        # Determine chapter type and extract title
        title_patterns = [
            (r'\\chapterwithsummaryfromfile\[[^\]]*\]\{([^}]+)\}', 'chapterwithsummaryfromfile'),
            (r'\\chapterwithsummary\[[^\]]*\]\{([^}]+)\}', 'chapterwithsummary'),
            (r'\\chapter\[[^\]]*\]\{([^}]+)\}', 'chapter_with_optional'),
            (r'\\chapter\{([^}]+)\}', 'chapter_simple')
        ]
        
        for pattern, ctype in title_patterns:
            title_match = re.search(pattern, block_content)
            if title_match:
                chapter_title = title_match.group(1)
                chapter_type = ctype
                break
        
        # Extract label
        label_match = re.search(r'\\chapterwithsummaryfromfile\[([^\]]+)\]', block_content)
        if not label_match:
            label_match = re.search(r'\\chapterwithsummary\[([^\]]+)\]', block_content)
        if not label_match:
            label_match = re.search(r'\\label\{([^}]+)\}', block_content)
        
        if label_match:
            label = label_match.group(1)
        
        # Extract file path
        file_match = re.search(r'\\inputstory\{([^}]+)\}', block_content)
        if file_match:
            file_path = file_match.group(1)
        
        is_enabled = ifdefined_name in enabled_chapters
        
        # Check if the input story file exists
        story_file_exists, story_file_path = check_file_exists(file_path)
        
        # For chapterwithsummaryfromfile, check if there's a summary file
        summary_file_exists = False
        summary_file_path = None
        if chapter_type == 'chapterwithsummaryfromfile':
            # The correct pattern is {folder}/summary.tex
            summary_candidate = f"{file_path}/summary.tex"
            exists, path = check_file_exists(summary_candidate)
            if exists:
                summary_file_exists = True
                summary_file_path = path
        
        chapters.append({
            'order': order,
            'ifdefined_name': ifdefined_name,
            'chapter_title': chapter_title,
            'label': label,
            'file_path': file_path,
            'chapter_type': chapter_type,
            'is_enabled': is_enabled,
            'status': 'ENABLED' if is_enabled else 'DISABLED',
            'story_file_exists': story_file_exists,
            'story_file_path': story_file_path,
            'summary_file_exists': summary_file_exists,
            'summary_file_path': summary_file_path,
            'has_summary_file': chapter_type == 'chapterwithsummaryfromfile'
        })
    
    return chapters


def main():
    """Main function to parse chapters and create DataFrame"""
    
    tex_file = Path('main.tex')
    
    if not tex_file.exists():
        print(f"Error: {tex_file} not found!")
        return
    
    print("Parsing main.tex for chapter information...")
    
    # Use the comprehensive extraction method
    chapters = extract_chapter_info_comprehensive(tex_file)
    
    if not chapters:
        print("No chapters found!")
        return
    
    # Create DataFrame
    df = pd.DataFrame(chapters)
    
    # Display results
    print(f"\nFound {len(chapters)} chapters:")
    print("=" * 80)
    
    # Show summary
    enabled_count = df['is_enabled'].sum()
    disabled_count = len(df) - enabled_count
    chapters_with_summary = df['has_summary_file'].sum()
    missing_story_files = (~df['story_file_exists']).sum()
    missing_summary_files = (df['has_summary_file'] & ~df['summary_file_exists']).sum()
    
    print(f"Summary: {enabled_count} enabled, {disabled_count} disabled chapters")
    print(f"Chapter types: {chapters_with_summary} use chapterwithsummaryfromfile")
    print(f"Missing files: {missing_story_files} story files, {missing_summary_files} summary files\n")
    
    # Display the DataFrame with better formatting
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 40)
    
    print("Full Chapter List:")
    display_columns = ['order', 'chapter_title', 'chapter_type', 'is_enabled', 'story_file_exists', 'summary_file_exists']
    print(df[display_columns].to_string(index=False))
    
    # Show only enabled chapters
    enabled_df = df[df['is_enabled'] == True]
    if not enabled_df.empty:
        print(f"\n\nCurrently Enabled Chapters ({len(enabled_df)}):")
        print("=" * 50)
        print(enabled_df[['order', 'chapter_title', 'file_path', 'story_file_exists']].to_string(index=False))
    
    # Show chapters with missing files
    missing_story_df = df[~df['story_file_exists']]
    if not missing_story_df.empty:
        print(f"\n\nChapters with Missing Story Files ({len(missing_story_df)}):")
        print("=" * 50)
        print(missing_story_df[['order', 'chapter_title', 'file_path']].to_string(index=False))
    
    missing_summary_df = df[df['has_summary_file'] & ~df['summary_file_exists']]
    if not missing_summary_df.empty:
        print(f"\n\nChapters with Missing Summary Files ({len(missing_summary_df)}):")
        print("=" * 50)
        print(missing_summary_df[['order', 'chapter_title', 'file_path']].to_string(index=False))
    
    # Save to CSV
    output_file = 'utils/chapters_analysis.csv'
    df.to_csv(output_file, index=False)
    print(f"\n\nData saved to: {output_file}")
    
    return df


if __name__ == "__main__":
    df = main() 