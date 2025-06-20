#!/usr/bin/env python3
"""
Generate four prime gap visualization plots for Chapter 08: Bounded Prime Gaps
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import ConnectionPatch
import matplotlib.patches as mpatches

def sieve_of_eratosthenes(limit):
    """Generate all primes up to limit using Sieve of Eratosthenes"""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = False
    
    return [i for i in range(2, limit + 1) if sieve[i]]

def plot_numbers_with_primes(max_n=25):
    """Plot 1: Natural numbers 1-25 as vertical lines, primes colored differently"""
    primes = set(sieve_of_eratosthenes(max_n))
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot all numbers as vertical lines
    for n in range(1, max_n + 1):
        if n in primes:
            ax.axvline(x=n, color='red', linewidth=3, alpha=0.8, label='Prime' if n == 2 else "")
        else:
            ax.axvline(x=n, color='lightgray', linewidth=2, alpha=0.6, label='Composite' if n == 4 else "")
    
    # Add number labels
    for n in range(1, max_n + 1):
        ax.text(n, -0.15, str(n), ha='center', va='top', fontsize=10, 
               color='red' if n in primes else 'black',
               weight='bold' if n in primes else 'normal')
    
    ax.set_xlim(0.5, max_n + 0.5)
    ax.set_ylim(-0.3, 1)
    ax.set_xlabel('Natural Numbers', fontsize=12)
    ax.set_title('Natural Numbers 1-25: Primes vs Composites', fontsize=14, weight='bold')
    ax.set_yticks([])
    ax.grid(True, alpha=0.3)
    
    # Create custom legend
    prime_patch = mpatches.Patch(color='red', alpha=0.8, label='Prime Numbers')
    composite_patch = mpatches.Patch(color='lightgray', alpha=0.6, label='Composite Numbers')
    ax.legend(handles=[prime_patch, composite_patch], loc='upper right')
    
    plt.tight_layout()
    plt.savefig('plot1_numbers_primes.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_prime_gaps(max_n=25):
    """Plot 2: Prime vertical lines with horizontal arrows showing gaps"""
    primes = sieve_of_eratosthenes(max_n)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Plot prime vertical lines
    for p in primes:
        ax.axvline(x=p, color='red', linewidth=3, alpha=0.8)
        ax.text(p, -0.15, str(p), ha='center', va='top', fontsize=10, 
               color='red', weight='bold')
    
    # Add gap arrows and labels
    for i in range(len(primes) - 1):
        p1, p2 = primes[i], primes[i + 1]
        gap = p2 - p1
        
        # Horizontal double-headed arrow
        y_pos = 0.3 + (i % 3) * 0.2  # Stagger heights to avoid overlap
        
        arrow = FancyArrowPatch((p1, y_pos), (p2, y_pos),
                               arrowstyle='<->', 
                               color='blue', 
                               linewidth=2,
                               mutation_scale=15)
        ax.add_patch(arrow)
        
        # Gap label
        ax.text((p1 + p2) / 2, y_pos + 0.1, f'gap={gap}', 
               ha='center', va='bottom', fontsize=9, 
               color='blue', weight='bold')
    
    ax.set_xlim(1.5, max_n + 0.5)
    ax.set_ylim(-0.3, 1.2)
    ax.set_xlabel('Prime Numbers', fontsize=12)
    ax.set_title('Prime Gaps: Distances Between Consecutive Primes', fontsize=14, weight='bold')
    ax.set_yticks([])
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plot2_prime_gaps.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_gap_scatter(max_prime=1000000):
    """Plot 3: Prime gap scatter plot with reference lines"""
    primes = sieve_of_eratosthenes(max_prime)
    gaps = [primes[i+1] - primes[i] for i in range(len(primes) - 1)]
    prime_starts = primes[:-1]  # p_n values
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Scatter plot with logarithmic x-axis
    ax.scatter(prime_starts, gaps, alpha=0.6, s=1, color='darkblue', label='Prime Gaps')
    
    # Set logarithmic scale for x-axis
    ax.set_xscale('log')
    
    # Reference lines with realistic values
    ax.axhline(y=2, color='red', linestyle='--', linewidth=2, alpha=0.8, 
              label='Twin Prime Gap (gap = 2)')
    ax.axhline(y=30, color='green', linestyle='--', linewidth=2, alpha=0.8, 
              label='Polymath8 Bound (gap ≤ 30)')
    ax.axhline(y=70, color='orange', linestyle='--', linewidth=2, alpha=0.8, 
              label="Zhang's Original Bound (gap ≤ 70)")
    
    # Add annotations with log-scale positioning
    ax.annotate('Twin Primes\n(conjectured infinite)', 
               xy=(10**5, 2), xytext=(10**5, 8),
               arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
               fontsize=10, ha='center', color='red')
    
    ax.annotate('Polymath8\nBound (proven)', 
               xy=(10**5, 30), xytext=(10**5, 40),
               arrowprops=dict(arrowstyle='->', color='green', alpha=0.7),
               fontsize=10, ha='center', color='green')
    
    ax.annotate("Zhang's Original\nBreakthrough", 
               xy=(10**5, 70), xytext=(10**5, 85),
               arrowprops=dict(arrowstyle='->', color='orange', alpha=0.7),
               fontsize=10, ha='center', color='orange')
    
    ax.set_xlabel('Prime Number ($p_n$) [Log Scale]', fontsize=12)
    ax.set_ylabel('Gap Size ($p_{n+1} - p_n$)', fontsize=12)
    ax.set_title('Prime Gap Distribution: Proving Infinitely Many Bounded Gaps', 
                fontsize=14, weight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left')
    
    # Remove y-axis tick labels (keep axis for reference only)
    ax.set_yticks([])
    
    # Set y-axis limit to 0-100
    ax.set_ylim(0, 100)
    
    plt.tight_layout()
    plt.savefig('plot3_gap_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_combined_figure():
    """Create a single figure with all four plots as subplots"""
    fig = plt.figure(figsize=(12, 24))
    
    # Plot 1: Natural numbers with primes highlighted
    ax1 = fig.add_subplot(4, 1, 1)
    max_n = 25
    primes = set(sieve_of_eratosthenes(max_n))
    
    # Plot all numbers as vertical lines
    for n in range(1, max_n + 1):
        if n in primes:
            ax1.axvline(x=n, color='red', linewidth=3, alpha=0.8, label='Prime' if n == 2 else "")
        else:
            ax1.axvline(x=n, color='teal', linewidth=2, alpha=0.6, label='Composite' if n == 4 else "")
    
    # Add number labels
    for n in range(1, max_n + 1):
        ax1.text(n, -0.15, str(n), ha='center', va='top', fontsize=8, 
               color='red' if n in primes else 'teal',
               weight='bold' if n in primes else 'normal')
    
    ax1.set_xlim(0.5, max_n + 0.5)
    ax1.set_ylim(-0.3, 1)
    ax1.set_xlabel('Natural Numbers', fontsize=10)
    ax1.set_title('Numbers 1-25:\nPrimes vs Composites', fontsize=12, weight='bold')
    ax1.set_yticks([])
    ax1.grid(True, alpha=0.3)
    
    # Set x-tick on each number
    ax1.set_xticks(range(1, max_n + 1))
    
    # Create custom legend
    prime_patch = mpatches.Patch(color='red', alpha=0.8, label='Prime Numbers')
    composite_patch = mpatches.Patch(color='teal', alpha=0.6, label='Composite Numbers')
    ax1.legend(handles=[prime_patch, composite_patch], loc='upper right', fontsize=8)
    
    # Remove box/spines from subplot 1
    for spine in ax1.spines.values():
        spine.set_visible(False)
    
    # Plot 2: Prime gaps with arrows
    ax2 = fig.add_subplot(4, 1, 2)
    primes_list = sieve_of_eratosthenes(max_n)
    
    # Plot prime vertical lines
    for p in primes_list:
        ax2.axvline(x=p, color='red', linewidth=3, alpha=0.8)
        ax2.text(p, -0.15, str(p), ha='center', va='top', fontsize=8, 
               color='red', weight='bold')
    
    # Add gap arrows and labels
    for i in range(len(primes_list) - 1):
        p1, p2 = primes_list[i], primes_list[i + 1]
        gap = p2 - p1
        
        # Horizontal double-headed arrow
        y_pos = 0.3 + (i % 3) * 0.2  # Stagger heights to avoid overlap
        
        arrow = FancyArrowPatch((p1, y_pos), (p2, y_pos),
                               arrowstyle='<->', 
                               color='blue', 
                               linewidth=2,
                               mutation_scale=15)
        ax2.add_patch(arrow)
        
        # Gap label
        ax2.text((p1 + p2) / 2, y_pos + 0.1, f'gap={gap}', 
               ha='center', va='bottom', fontsize=7, 
               color='blue', weight='bold')
    
    ax2.set_xlim(1.5, max_n + 0.5)
    ax2.set_ylim(-0.3, 1.2)
    ax2.set_xlabel('Prime Numbers', fontsize=10)
    ax2.set_title('Prime Gaps:\nDistances Between Primes', fontsize=12, weight='bold')
    ax2.set_yticks([])
    ax2.grid(True, alpha=0.3)
    
    # Set x-tick on each prime number
    ax2.set_xticks(primes_list)
    
    # Remove box/spines from subplot 2
    for spine in ax2.spines.values():
        spine.set_visible(False)
    
    # Plot 3: Prime gap scatter plot with corrected legend
    ax3 = fig.add_subplot(4, 1, 3)
    max_prime = 100000  # Use same range as plot 4
    primes_large = sieve_of_eratosthenes(max_prime)
    gaps = [primes_large[i+1] - primes_large[i] for i in range(len(primes_large) - 1)]
    prime_starts = primes_large[:-1]  # p_n values
    
    # Scatter plot with logarithmic x-axis
    ax3.scatter(prime_starts, gaps, alpha=0.6, s=1, color='darkblue', label='Prime Gaps')
    
    # Set logarithmic scale for x-axis
    ax3.set_xscale('log')
    
    # Reference lines with corrected legend labels showing actual bounds
    ax3.axhline(y=2, color='red', linestyle='--', linewidth=2, alpha=0.8, 
              label='Twin Prime Gap (gap = 2)')
    ax3.axhline(y=30, color='green', linestyle='--', linewidth=2, alpha=0.8, 
              label='Polymath8 Bound (gap ≤ 246)')
    ax3.axhline(y=70, color='orange', linestyle='--', linewidth=2, alpha=0.8, 
              label="Zhang's Original Bound (gap ≤ 70M)")
    
    # Add annotations with log-scale positioning
    ax3.annotate('Twin Primes\n(conjectured infinite)', 
               xy=(10**5, 2), xytext=(10**5, 8),
               arrowprops=dict(arrowstyle='->', color='red', alpha=0.7),
               fontsize=8, ha='center', color='red')
    
    ax3.annotate('Polymath8\nBound (proven)', 
               xy=(10**5, 30), xytext=(10**5, 40),
               arrowprops=dict(arrowstyle='->', color='green', alpha=0.7),
               fontsize=8, ha='center', color='green')
    
    ax3.annotate("Zhang's Original\nBreakthrough", 
               xy=(10**5, 70), xytext=(10**5, 85),
               arrowprops=dict(arrowstyle='->', color='orange', alpha=0.7),
               fontsize=8, ha='center', color='orange')
    
    ax3.set_xlabel('Prime Number ($p_n$) [Log Scale]', fontsize=10)
    ax3.set_ylabel('Gap Size ($p_{n+1} - p_n$)', fontsize=10)
    ax3.set_title('Prime Gap Distribution:\nProving Infinitely Many Bounded Gaps', 
                fontsize=12, weight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc='upper left', fontsize=8)
    
    # Remove y-axis tick labels (keep axis for reference only)
    ax3.set_yticks([])
    
    # Remove x-axis ticks and labels
    ax3.set_xticks([])
    ax3.set_xticklabels([])
    
    # Set axis limits to match plot 4
    ax3.set_xlim(100, 1e5)
    ax3.set_ylim(0, 100)
    
    # Remove box/spines from subplot 3
    for spine in ax3.spines.values():
        spine.set_visible(False)
    
    # Plot 4: Theoretical bounds for large prime gaps
    ax4 = fig.add_subplot(4, 1, 4)
    
    # Generate range of p_n values (log scale)
    p_values = np.logspace(2, 6, 1000)  # From 100 to 1,000,000
    log_p = np.log(p_values)
    log_log_p = np.log(log_p)
    log_log_log_p = np.log(log_log_p)
    log_log_log_log_p = np.log(log_log_log_p)
    
    # Use the same scatter data as plot 3
    # Scatter plot of actual gaps with bigger dots
    ax4.scatter(prime_starts, gaps, alpha=0.4, s=3, color='lightblue', 
               label='Actual Prime Gaps', zorder=1)
    
    # Upper bounds
    # Cramér conjecture: G(x) ~ (log x)²
    cramer_upper = (log_p)**2
    ax4.plot(p_values, cramer_upper, 'r-', linewidth=2, alpha=0.8, 
             label='Cramér Conjecture: $(\\log p_n)^2$', zorder=3)
    
    # Granville refinement: G(x) ≥ 2e^(-γ)(log x)²
    gamma = 0.5772156649  # Euler-Mascheroni constant
    granville_lower = 2 * np.exp(-gamma) * (log_p)**2
    ax4.plot(p_values, granville_lower, 'r--', linewidth=2, alpha=0.8,
             label='Granville Lower: $2e^{-\\gamma}(\\log p_n)^2$', zorder=3)
    
    # Lower bounds
    # Latest result (2014): Ford-Green-Konyagin-Maynard-Tao
    # G(x) ≥ c log x · log log x · log log log log x / log log log x
    fgkmt_lower = 0.1 * log_p * log_log_p * log_log_log_log_p / log_log_log_p
    ax4.plot(p_values, fgkmt_lower, 'darkgreen', linewidth=2, alpha=0.8,
             label='FGKMT 2014: Large Gap Lower Bound', zorder=3)
    
    # Rankin bound (1938)
    rankin_lower = 0.05 * log_p * log_log_p * log_log_log_log_p / (log_log_log_p)**2
    ax4.plot(p_values, rankin_lower, 'darkblue', linewidth=2, alpha=0.8,
             label='Rankin 1938: Classic Lower Bound', zorder=3)
    
    # Prime Number Theorem trivial bound
    pnt_lower = 0.9 * log_p
    ax4.plot(p_values, pnt_lower, 'purple', linewidth=2, alpha=0.8,
             label='PNT Lower: $(1-\\epsilon)\\log p_n$', zorder=3)
    
    ax4.set_xscale('log')
    ax4.set_yscale('log')
    ax4.set_xlabel('Prime Number $p_n$ (Log Scale)', fontsize=10)
    ax4.set_ylabel('Gap Size G($p_n$) (Log Scale)', fontsize=10)
    ax4.grid(True, alpha=0.3)
    ax4.legend(loc='upper left', fontsize=8)
    ax4.set_title('Large Prime Gaps: Actual Data vs Theoretical Bounds\\n(Scatter: Real Gaps, Lines: Theory)', 
                 fontsize=12, weight='bold')
    
    # Set reasonable axis limits to show the data well
    ax4.set_xlim(100, 1e5)
    ax4.set_ylim(1, 1000)
    
    plt.tight_layout()
    plt.savefig('prime_gaps_combined.pdf', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Generate the combined four-subplot figure"""
    print("Generating combined prime gap visualization...")
    
    print("Creating combined figure with all four plots...")
    create_combined_figure()
    
    print("Combined figure generated successfully!")
    print("File created: prime_gaps_combined.pdf")

if __name__ == "__main__":
    main() 