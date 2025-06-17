#!/usr/bin/env python3
"""
Incremental LaTeX compilation system.
Compiles only changed chapters individually for fast development feedback.
"""

import subprocess
import time
import threading
import os
import re
import json
import shutil
from datetime import datetime
from pathlib import Path

class IncrementalCompiler:
    def __init__(self):
        self.cache_file = '.incremental_cache.json'
        self.temp_dir = '.incremental_temp'
        self.output_dir = 'incremental_pdfs'
        
    def get_file_state(self, filepath):
        """Get file modification time and size."""
        try:
            stat = os.stat(filepath)
            return {
                'mtime': stat.st_mtime,
                'size': stat.st_size
            }
        except:
            return None
    
    def get_chapter_state(self, chapter_dir):
        """Get state of all files in a chapter directory."""
        state = {}
        if os.path.exists(chapter_dir):
            for root, dirs, files in os.walk(chapter_dir):
                for file in files:
                    if file.endswith(('.tex', '.png', '.jpg', '.jpeg', '.pdf', '.eps')):
                        filepath = os.path.join(root, file)
                        rel_path = os.path.relpath(filepath, '.')
                        state[rel_path] = self.get_file_state(filepath)
        return state
    
    def load_cache(self):
        """Load incremental cache."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {'chapters': {}}
    
    def save_cache(self, cache_data):
        """Save incremental cache."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save cache: {e}")
    
    def detect_changed_chapters(self):
        """Detect which chapters have changed since last compilation."""
        cache = self.load_cache()
        changed_chapters = []
        
        # Scan all chapter directories
        for item in os.listdir('.'):
            if os.path.isdir(item) and re.match(r'(\d+)_(.+)', item):
                match = re.match(r'(\d+)_(.+)', item)
                chapter_num = int(match.group(1))
                chapter_name = match.group(2)
                
                current_state = self.get_chapter_state(item)
                cached_state = cache['chapters'].get(item, {})
                
                # Check if anything changed
                if current_state != cached_state:
                    changed_chapters.append({
                        'number': chapter_num,
                        'name': chapter_name,
                        'directory': item,
                        'state': current_state
                    })
        
        # Sort by chapter number
        changed_chapters.sort(key=lambda x: x['number'])
        return changed_chapters, cache
    
    def create_minimal_document(self, chapter_dir, chapter_num, chapter_name):
        """Create a minimal LaTeX document for a single chapter."""
        
        # Read the main preamble
        preamble_content = ""
        if os.path.exists('preamble.tex'):
            with open('preamble.tex', 'r') as f:
                preamble_content = f.read()
        
        # Create minimal document
        doc_content = f"""\\documentclass{{book}}

% Include main preamble
{preamble_content}

\\begin{{document}}

% Set chapter counter
\\setcounter{{chapter}}{{{chapter_num - 1}}}

% Include chapter content
\\input{{{chapter_dir}/title.tex}}
\\input{{{chapter_dir}/summary.tex}}  
\\input{{{chapter_dir}/main.tex}}

\\end{{document}}
"""
        
        return doc_content
    
    def compile_chapter(self, chapter_info):
        """Compile a single chapter quickly."""
        chapter_dir = chapter_info['directory']
        chapter_num = chapter_info['number']
        chapter_name = chapter_info['name']
        
        print(f"🔄 Compiling Chapter {chapter_num:02d}: {chapter_name}")
        
        # Create temp directory
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Create minimal document
        doc_content = self.create_minimal_document(chapter_dir, chapter_num, chapter_name)
        temp_tex = os.path.join(self.temp_dir, f'chapter_{chapter_num:02d}.tex')
        
        with open(temp_tex, 'w') as f:
            f.write(doc_content)
        
        # Copy chapter files to temp directory
        temp_chapter_dir = os.path.join(self.temp_dir, chapter_dir)
        if os.path.exists(temp_chapter_dir):
            shutil.rmtree(temp_chapter_dir)
        shutil.copytree(chapter_dir, temp_chapter_dir)
        
        # Copy any needed assets
        for asset_dir in ['images', 'utils']:
            if os.path.exists(asset_dir):
                temp_asset_dir = os.path.join(self.temp_dir, asset_dir)
                if os.path.exists(temp_asset_dir):
                    shutil.rmtree(temp_asset_dir)
                shutil.copytree(asset_dir, temp_asset_dir)
        
        start_time = time.time()
        
        # Compile with lualatex
        try:
            result = subprocess.run([
                'lualatex', 
                '-interaction=nonstopmode',
                '-output-directory', self.temp_dir,
                temp_tex
            ], 
            capture_output=True, 
            text=True, 
            cwd='.',
            timeout=60  # 1 minute timeout for single chapter
            )
            
            compile_time = time.time() - start_time
            
            # Check if PDF was generated
            temp_pdf = os.path.join(self.temp_dir, f'chapter_{chapter_num:02d}.pdf')
            if os.path.exists(temp_pdf):
                # Move to output directory
                os.makedirs(self.output_dir, exist_ok=True)
                output_pdf = os.path.join(self.output_dir, f'chapter_{chapter_num:02d}_{chapter_name}.pdf')
                shutil.move(temp_pdf, output_pdf)
                
                pdf_size = os.path.getsize(output_pdf) / (1024*1024)
                print(f"  ✅ Chapter {chapter_num:02d} compiled in {compile_time:.1f}s → {pdf_size:.1f}MB")
                return True, output_pdf
            else:
                print(f"  ❌ Chapter {chapter_num:02d} compilation failed")
                if result.stderr:
                    print(f"     Error: {result.stderr[:200]}...")
                return False, None
                
        except subprocess.TimeoutExpired:
            print(f"  ❌ Chapter {chapter_num:02d} compilation timed out")
            return False, None
        except Exception as e:
            print(f"  ❌ Chapter {chapter_num:02d} compilation error: {e}")
            return False, None
    
    def cleanup_temp(self):
        """Clean up temporary files."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def format_time(self, seconds):
        """Format seconds into readable time."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        else:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
    
    def compile_incremental(self, force_all=False):
        """Main incremental compilation function."""
        print("🚀 INCREMENTAL LATEX COMPILATION")
        print("=" * 40)
        
        if force_all:
            print("🔄 Force mode: Compiling all chapters")
            # Get all chapters
            changed_chapters = []
            for item in os.listdir('.'):
                if os.path.isdir(item) and re.match(r'(\d+)_(.+)', item):
                    match = re.match(r'(\d+)_(.+)', item)
                    chapter_num = int(match.group(1))
                    chapter_name = match.group(2)
                    changed_chapters.append({
                        'number': chapter_num,
                        'name': chapter_name,
                        'directory': item,
                        'state': self.get_chapter_state(item)
                    })
            changed_chapters.sort(key=lambda x: x['number'])
            cache = self.load_cache()
        else:
            # Detect changes
            print("🔍 Detecting changed chapters...")
            changed_chapters, cache = self.detect_changed_chapters()
        
        if not changed_chapters:
            print("✨ No changes detected - all chapters up to date!")
            return True
        
        print(f"📝 Found {len(changed_chapters)} changed chapter(s):")
        for ch in changed_chapters:
            print(f"   • Chapter {ch['number']:02d}: {ch['name']}")
        
        # Clean up previous temp files
        self.cleanup_temp()
        
        overall_start = time.time()
        successful_compilations = 0
        
        # Compile each changed chapter
        for chapter_info in changed_chapters:
            success, pdf_path = self.compile_chapter(chapter_info)
            if success:
                successful_compilations += 1
                # Update cache for this chapter
                cache['chapters'][chapter_info['directory']] = chapter_info['state']
        
        total_time = time.time() - overall_start
        
        print(f"\n🏁 INCREMENTAL COMPILATION COMPLETE")
        print(f"⏱️  Total time: {self.format_time(total_time)}")
        print(f"✅ Successfully compiled: {successful_compilations}/{len(changed_chapters)} chapters")
        
        if successful_compilations > 0:
            print(f"📁 Individual PDFs saved to: {self.output_dir}/")
            
        # Save updated cache
        self.save_cache(cache)
        
        # Clean up
        self.cleanup_temp()
        
        return successful_compilations == len(changed_chapters)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Incremental LaTeX compilation')
    parser.add_argument('--all', action='store_true', 
                       help='Force compile all chapters (ignore cache)')
    parser.add_argument('--full', action='store_true',
                       help='Also run full document compilation after incremental')
    args = parser.parse_args()
    
    compiler = IncrementalCompiler()
    success = compiler.compile_incremental(force_all=args.all)
    
    if args.full and success:
        print("\n" + "="*50)
        print("🚀 RUNNING FULL DOCUMENT COMPILATION")
        print("="*50)
        
        # Run the smart compiler for full document
        result = subprocess.run(['python3', 'utils/compile_realtime_smart.py'], cwd='.')
        success = success and (result.returncode == 0)
    
    exit(0 if success else 1)

if __name__ == "__main__":
    main() 