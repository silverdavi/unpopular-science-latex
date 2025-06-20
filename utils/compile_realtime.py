#!/usr/bin/env python3
"""
Real-time LaTeX compilation with progress tracking and live updates.
"""

import subprocess
import time
import threading
import os
import re
from datetime import datetime, timedelta

class RealTimeCompiler:
    def __init__(self):
        self.start_time = None
        self.current_chapter = 0
        self.total_chapters = 0
        self.phase = "Initializing"
        self.log_lines = []
        self.process = None
        self.monitoring = True
        
    def count_chapters(self):
        """Count total chapters by looking for chapterwithsummaryfromfile statements."""
        try:
            with open('main.tex', 'r') as f:
                content = f.read()
            # Since we removed all \ifdefined blocks, count chapterwithsummaryfromfile directly
            chapter_count = len(re.findall(r'\\chapterwithsummaryfromfile', content))
            return chapter_count
        except:
            return 50  # fallback estimate
    
    def extract_chapter_info(self, line):
        """Extract chapter information from log line."""
        # Look for chapter files being processed
        if '/' in line and any(ext in line for ext in ['title.tex', 'summary.tex', 'main.tex']):
            # Extract chapter number from path like "./01_BanachTarskiParadox/title.tex"
            match = re.search(r'(\d+)_([^/]+)/', line)
            if match:
                chapter_num = int(match.group(1))
                chapter_name = match.group(2)
                return chapter_num, chapter_name
        return None, None
    
    def clean_build_artifacts(self):
        """Clean all build artifacts from previous compilations."""
        print("🧹 Cleaning build artifacts...")
        
        # LaTeX build files
        latex_extensions = [
            'aux', 'toc', 'log', 'out', 'fdb_latexmk', 'fls', 'synctex.gz',
            'bbl', 'blg', 'idx', 'ind', 'ilg', 'lof', 'lot', 'nav', 'snm', 'vrb'
        ]
        
        cleaned_count = 0
        
        # Clean main document artifacts
        for ext in latex_extensions:
            file_path = f'main.{ext}'
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    cleaned_count += 1
                except Exception as e:
                    print(f"  ⚠️  Could not remove {file_path}: {e}")
        
        # Clean compilation log files
        for log_file in ['compile_pass1.log', 'compile_pass2.log']:
            if os.path.exists(log_file):
                try:
                    os.remove(log_file)
                    cleaned_count += 1
                except Exception as e:
                    print(f"  ⚠️  Could not remove {log_file}: {e}")
        
        # Clean any LaTeX auxiliary files in subdirectories
        for root, dirs, files in os.walk('.'):
            for file in files:
                if any(file.endswith(f'.{ext}') for ext in latex_extensions):
                    file_path = os.path.join(root, file)
                    # Skip main.pdf and other important PDFs
                    if not file.endswith('.pdf') or file.startswith('main.'):
                        try:
                            os.remove(file_path)
                            cleaned_count += 1
                        except Exception as e:
                            pass  # Silent fail for subdirectory cleanup
        
        print(f"  ✅ Cleaned {cleaned_count} build artifacts")
    
    def format_time(self, seconds):
        """Format seconds into readable time."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}m {secs}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def estimate_remaining_time(self, elapsed, progress):
        """Estimate remaining compilation time."""
        if progress > 0.05:  # Only estimate after 5% progress
            total_estimated = elapsed / progress
            remaining = total_estimated - elapsed
            return max(0, remaining)
        return None
    
    def print_progress(self, chapter_num, chapter_name, elapsed):
        """Print current progress with time estimates."""
        if self.total_chapters > 0:
            progress = chapter_num / self.total_chapters
            bar_length = 40
            filled_length = int(bar_length * progress)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)
            
            remaining_time = self.estimate_remaining_time(elapsed, progress)
            remaining_str = f" | ETA: {self.format_time(remaining_time)}" if remaining_time else ""
            
            print(f"\r🔄 [{bar}] {progress*100:.1f}% | Ch.{chapter_num:02d}: {chapter_name[:20]:<20} | {self.format_time(elapsed)}{remaining_str}", end="", flush=True)
    
    def monitor_log_file(self, log_file):
        """Monitor log file in real-time."""
        last_pos = 0
        mystery_strings = []
        
        while self.monitoring:
            try:
                if os.path.exists(log_file):
                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        f.seek(last_pos)
                        new_lines = f.readlines()
                        last_pos = f.tell()
                        
                        for line in new_lines:
                            line = line.strip()
                            if line:
                                self.log_lines.append(line)
                                
                                # Check for mystery strings
                                if re.match(r'^\d+show[A-Za-z]+$', line):
                                    mystery_strings.append(line)
                                    print(f"\n🔍 Mystery string detected: '{line}'")
                                
                                # Extract chapter info
                                chapter_num, chapter_name = self.extract_chapter_info(line)
                                if chapter_num and chapter_name:
                                    self.current_chapter = max(self.current_chapter, chapter_num)
                                    elapsed = time.time() - self.start_time
                                    self.print_progress(chapter_num, chapter_name, elapsed)
                                
                                # Check for completion
                                if "Output written on" in line:
                                    self.phase = "Completed"
                                    self.pdf_generated = True
                                    match = re.search(r'(\d+) pages.*?(\d+) bytes', line)
                                    if match:
                                        pages, size_bytes = match.groups()
                                        size_mb = int(size_bytes) / (1024*1024)
                                        print(f"\n✅ PDF generated: {pages} pages, {size_mb:.1f}MB")
                                
                                # Check for errors (but ignore normal LaTeX loading messages)
                                if any(err in line.lower() for err in ['error', 'emergency stop', '! ']):
                                    # Ignore false positives: file paths, loading messages, and warnings
                                    if ('warning' not in line.lower() and 
                                        not line.strip().startswith('(') and  # File loading paths
                                        '.code.tex' not in line and           # LaTeX code files
                                        '.sty' not in line and                # Style files
                                        'errorbars.cod' not in line):          # Specific pgfplots false positive
                                        print(f"\n❌ Error detected: {line}")
                
                time.sleep(0.1)  # Check every 100ms
            except Exception as e:
                time.sleep(0.5)
        
        return mystery_strings
    
    def compile_pass(self, pass_num, log_file):
        """Compile a single pass with monitoring."""
        print(f"\n📚 Pass {pass_num}: {'Building document structure' if pass_num == 1 else 'Finalizing cross-references'}")
        
        self.start_time = time.time()
        self.current_chapter = 0
        self.monitoring = True
        self.pdf_generated = False
        
        # Start log monitoring in background
        log_thread = threading.Thread(target=self.monitor_log_file, args=(log_file,))
        log_thread.daemon = True
        log_thread.start()
        
        # Start compilation
        cmd = ['lualatex', '-interaction=nonstopmode', 'main.tex']
        self.process = subprocess.Popen(
            cmd, 
            stdout=open(log_file, 'w'), 
            stderr=subprocess.STDOUT,
            cwd='.'
        )
        
        # Wait for completion
        return_code = self.process.wait()
        self.monitoring = False
        
        elapsed = time.time() - self.start_time
        
        # Success is determined by PDF generation, not exit code (LaTeX can have warnings)
        success = self.pdf_generated or os.path.exists('main.pdf')
        
        if success:
            print(f"\n✅ Pass {pass_num} completed in {self.format_time(elapsed)}")
        else:
            print(f"\n❌ Pass {pass_num} failed after {self.format_time(elapsed)}")
            
        return success
    
    def compile_document(self):
        """Compile the document with real-time progress."""
        print("🚀 REAL-TIME LATEX COMPILATION")
        print("=" * 50)
        
        # Count chapters
        self.total_chapters = self.count_chapters()
        print(f"📖 Detected {self.total_chapters} chapters")
        
        # Clean old files
        self.clean_build_artifacts()
        
        overall_start = time.time()
        
        # First pass
        success1 = self.compile_pass(1, 'compile_pass1.log')
        if not success1:
            print("❌ First pass failed, aborting.")
            return False
        
        # Second pass  
        success2 = self.compile_pass(2, 'compile_pass2.log')
        
        total_time = time.time() - overall_start
        
        print(f"\n🏁 COMPILATION COMPLETE")
        print(f"⏱️  Total time: {self.format_time(total_time)}")
        
        # Check final results
        if os.path.exists('main.pdf'):
            pdf_size = os.path.getsize('main.pdf') / (1024*1024)
            print(f"📄 PDF: {pdf_size:.1f}MB")
        
        if os.path.exists('main.toc'):
            toc_size = os.path.getsize('main.toc')
            if toc_size > 0:
                print(f"📑 ToC: {toc_size} bytes")
            else:
                print("⚠️  ToC is empty (0 bytes) - check for issues!")
        
        return success1 and success2

def main():
    compiler = RealTimeCompiler()
    success = compiler.compile_document()
    exit(0 if success else 1)

if __name__ == "__main__":
    main() 