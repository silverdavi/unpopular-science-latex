#!/usr/bin/env python3

"""
Advanced LaTeX Compilation Script with Performance Analytics
Provides detailed timing, memory usage, and compilation statistics
"""

import subprocess
import time
import os
import re
import sys
from pathlib import Path
import psutil
import threading
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class CompilationStats:
    step_name: str
    duration: float
    pages: int
    pdf_size_mb: float
    peak_memory_mb: float
    cpu_percent: float
    success: bool
    warnings: int
    errors: int

class LaTeXCompiler:
    def __init__(self, tex_file: str = "main.tex"):
        self.tex_file = tex_file
        self.stats: List[CompilationStats] = []
        self.monitoring = False
        self.peak_memory = 0
        self.cpu_usage = []
        
    def monitor_resources(self):
        """Monitor system resources during compilation"""
        process = psutil.Process()
        while self.monitoring:
            try:
                memory_mb = process.memory_info().rss / 1024 / 1024
                cpu_percent = process.cpu_percent()
                self.peak_memory = max(self.peak_memory, memory_mb)
                self.cpu_usage.append(cpu_percent)
                time.sleep(0.1)
            except:
                break
    
    def start_monitoring(self):
        """Start resource monitoring in background thread"""
        self.monitoring = True
        self.peak_memory = 0
        self.cpu_usage = []
        monitor_thread = threading.Thread(target=self.monitor_resources)
        monitor_thread.daemon = True
        monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop resource monitoring"""
        self.monitoring = False
        time.sleep(0.2)  # Let monitoring thread finish
    
    def get_pdf_stats(self) -> tuple:
        """Get PDF page count and size"""
        if not os.path.exists("main.pdf"):
            return 0, 0.0
        
        # Get file size
        size_bytes = os.path.getsize("main.pdf")
        size_mb = size_bytes / (1024 * 1024)
        
        # Get page count from log
        pages = 0
        if os.path.exists("main.log"):
            with open("main.log", "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                matches = re.findall(r"Output written.*?\((\d+) pages?", content)
                if matches:
                    pages = int(matches[-1])
        
        return pages, size_mb
    
    def count_warnings_errors(self, log_file: str) -> tuple:
        """Count warnings and errors in log file"""
        if not os.path.exists(log_file):
            return 0, 0
        
        warnings = 0
        errors = 0
        
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if re.search(r"warning", line, re.IGNORECASE):
                    warnings += 1
                if re.search(r"error", line, re.IGNORECASE):
                    errors += 1
        
        return warnings, errors
    
    def run_lualatex(self, pass_name: str, log_file: str) -> bool:
        """Run LuaLaTeX compilation with monitoring"""
        print(f"🔄 Running {pass_name}...")
        
        # Start resource monitoring
        self.start_monitoring()
        start_time = time.time()
        
        # Run compilation
        try:
            result = subprocess.run(
                ["lualatex", "--interaction=nonstopmode", self.tex_file],
                stdout=open(log_file, "w"),
                stderr=subprocess.STDOUT,
                timeout=300  # 5 minute timeout
            )
            success = result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"❌ {pass_name} timed out after 5 minutes")
            success = False
        except Exception as e:
            print(f"❌ {pass_name} failed: {e}")
            success = False
        
        # Stop monitoring and calculate stats
        end_time = time.time()
        self.stop_monitoring()
        duration = end_time - start_time
        
        # Get compilation statistics
        pages, pdf_size_mb = self.get_pdf_stats()
        avg_cpu = sum(self.cpu_usage) / len(self.cpu_usage) if self.cpu_usage else 0
        warnings, errors = self.count_warnings_errors("main.log")
        
        # Record stats
        stats = CompilationStats(
            step_name=pass_name,
            duration=duration,
            pages=pages,
            pdf_size_mb=pdf_size_mb,
            peak_memory_mb=self.peak_memory,
            cpu_percent=avg_cpu,
            success=success,
            warnings=warnings,
            errors=errors
        )
        self.stats.append(stats)
        
        # Print immediate results
        status = "✅" if success else "❌"
        print(f"{status} {pass_name} completed in {duration:.2f}s")
        if pages > 0:
            print(f"   📄 {pages} pages, {pdf_size_mb:.2f} MB")
        print(f"   🧠 Memory: {self.peak_memory:.1f} MB, CPU: {avg_cpu:.1f}%")
        if warnings > 0 or errors > 0:
            print(f"   ⚠️  {warnings} warnings, {errors} errors")
        print()
        
        return success
    
    def clean_artifacts(self):
        """Clean previous build artifacts"""
        print("🧹 Cleaning build artifacts...")
        
        artifacts = [
            "*.aux", "*.log", "*.out", "*.toc", "*.lot", "*.lof",
            "*.synctex.gz", "*.fls", "*.fdb_latexmk", "*.idx", 
            "*.ilg", "*.ind", "main.pdf"
        ]
        
        start_time = time.time()
        cleaned = 0
        
        for pattern in artifacts:
            for file in Path(".").glob(pattern):
                try:
                    file.unlink()
                    cleaned += 1
                except:
                    pass
        
        duration = time.time() - start_time
        print(f"✅ Cleaned {cleaned} files in {duration:.3f}s\n")
        
        return duration
    
    def print_summary(self):
        """Print detailed compilation summary"""
        print("=" * 60)
        print("📊 DETAILED COMPILATION ANALYSIS")
        print("=" * 60)
        print()
        
        # Overall statistics
        total_time = sum(stat.duration for stat in self.stats)
        successful_passes = sum(1 for stat in self.stats if stat.success)
        final_stats = self.stats[-1] if self.stats else None
        
        print("🕐 TIMING BREAKDOWN:")
        for i, stat in enumerate(self.stats, 1):
            status = "✅" if stat.success else "❌"
            print(f"   {i}. {stat.step_name:<20} {stat.duration:>8.2f}s {status}")
        
        print(f"   {'Total Compilation:':<20} {total_time:>8.2f}s")
        print()
        
        if final_stats and final_stats.success:
            print("📈 PERFORMANCE METRICS:")
            print(f"   Pages per second:      {final_stats.pages / total_time:>8.2f}")
            print(f"   MB per second:         {final_stats.pdf_size_mb / total_time:>8.2f}")
            print(f"   Peak memory usage:     {max(s.peak_memory_mb for s in self.stats):>8.1f} MB")
            print(f"   Average CPU usage:     {sum(s.cpu_percent for s in self.stats) / len(self.stats):>8.1f}%")
            print()
            
            print("📄 OUTPUT STATISTICS:")
            print(f"   Final page count:      {final_stats.pages:>8} pages")
            print(f"   Final PDF size:        {final_stats.pdf_size_mb:>8.2f} MB")
            print(f"   Bytes per page:        {(final_stats.pdf_size_mb * 1024 * 1024) / final_stats.pages:>8.0f}")
            print()
        
        # Quality metrics
        total_warnings = sum(s.warnings for s in self.stats)
        total_errors = sum(s.errors for s in self.stats)
        
        print("🔍 QUALITY METRICS:")
        print(f"   Successful passes:     {successful_passes:>8} / {len(self.stats)}")
        print(f"   Total warnings:        {total_warnings:>8}")
        print(f"   Total errors:          {total_errors:>8}")
        
        if total_warnings > 0 or total_errors > 0:
            print(f"   Quality score:         {max(0, 100 - total_warnings * 2 - total_errors * 10):>8.0f}%")
        
        print()
        print("📁 Log files generated:")
        print("   - compile_pass1.log (first pass output)")
        print("   - compile_pass2.log (second pass output)")
        print("   - main.log (final LaTeX log)")
        print()

def main():
    if len(sys.argv) > 1:
        tex_file = sys.argv[1]
    else:
        tex_file = "main.tex"
    
    if not os.path.exists(tex_file):
        print(f"❌ Error: {tex_file} not found")
        sys.exit(1)
    
    compiler = LaTeXCompiler(tex_file)
    
    print("🚀 ADVANCED LATEX COMPILATION STARTED")
    print("=" * 60)
    print()
    
    # Clean artifacts
    clean_time = compiler.clean_artifacts()
    
    # First pass
    success1 = compiler.run_lualatex("First Pass", "compile_pass1.log")
    if not success1:
        print("❌ First pass failed, aborting compilation")
        sys.exit(1)
    
    # Second pass
    success2 = compiler.run_lualatex("Second Pass", "compile_pass2.log")
    
    # Print summary
    compiler.print_summary()
    
    # Final status
    if success1 and success2:
        print("🎉 Compilation completed successfully!")
        print(f"📄 Output: main.pdf")
    elif success1:
        print("⚠️  Compilation partially successful (first pass only)")
        print(f"📄 Output: main.pdf")
    else:
        print("❌ Compilation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 