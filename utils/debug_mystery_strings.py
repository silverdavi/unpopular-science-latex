#!/usr/bin/env python3
"""
Debug script to track down mystery variable names appearing in PDF output.
"""

import re
import subprocess
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF to search for mystery strings."""
    try:
        result = subprocess.run(['pdftotext', pdf_path, '-'], 
                              capture_output=True, text=True)
        return result.stdout
    except FileNotFoundError:
        print("⚠️  pdftotext not found. Install with: brew install poppler")
        return None

def find_mystery_strings_in_text(text):
    """Find variable names that shouldn't appear in the PDF."""
    pattern = r'\b\d{2}show[A-Za-z]+\b'
    matches = re.findall(pattern, text)
    return matches

def find_mystery_strings_in_pdf():
    """Search for mystery strings in the current PDF."""
    pdf_path = 'main.pdf'
    
    if not os.path.exists(pdf_path):
        print("❌ main.pdf not found")
        return
    
    print("🔍 Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    if text is None:
        print("❌ Could not extract text from PDF")
        return
    
    print("🔍 Searching for mystery strings...")
    mystery_strings = find_mystery_strings_in_text(text)
    
    if mystery_strings:
        print(f"❌ Found {len(mystery_strings)} mystery strings:")
        for string in set(mystery_strings):  # Remove duplicates
            print(f"   • {string}")
            
        # Show context around mystery strings
        print("\n🔍 Context around mystery strings:")
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if any(ms in line for ms in mystery_strings):
                start = max(0, i-2)
                end = min(len(lines), i+3)
                print(f"\nAround line {i+1}:")
                for j in range(start, end):
                    marker = ">>> " if j == i else "    "
                    print(f"{marker}{lines[j]}")
    else:
        print("✅ No mystery strings found in PDF text!")

def analyze_latex_logs():
    """Check LaTeX logs for any debug output that might cause mystery strings."""
    log_files = ['main.log', 'compile_pass1.log', 'compile_pass2.log']
    
    for log_file in log_files:
        if os.path.exists(log_file):
            print(f"\n🔍 Checking {log_file}...")
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                mystery_strings = find_mystery_strings_in_text(content)
                if mystery_strings:
                    print(f"   Found in log: {set(mystery_strings)}")
                else:
                    print("   Clean")

if __name__ == "__main__":
    print("🚀 MYSTERY STRING DEBUGGER")
    print("=" * 40)
    
    find_mystery_strings_in_pdf()
    analyze_latex_logs()
    
    print("\n💡 If mystery strings are found, they indicate variable names")
    print("   being output as text instead of being used as conditionals.") 