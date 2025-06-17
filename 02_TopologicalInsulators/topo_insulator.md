Here's the corrected and upgraded version of your guide, adjusted to reflect **2D, non-shaded**, parity-annotated schematic band structures like the figure you just posted. This version uses simplified geometric shapes, includes parity labeling, the \$\mathbb{Z}\_2\$ invariant, and explicitly shows the role of tuning SOC strength \$P\$ across the critical point \$P\_c\$.

---

## 🎯 Goal

Draw **three aligned subplots** (a, b, c) for:

* (a) Normal/Trivial Insulator (\$\mathbb{Z}\_2 = 0\$)
* (b) 2D Dirac Semimetal (Critical Point, \$P = P\_c\$)
* (c) Topological Insulator (\$\mathbb{Z}\_2 = 1\$)

Each plot shows valence and conduction bands, color-coded and annotated with parity eigenvalues (\$\pm\$), \$\mathbb{Z}\_2\$, Fermi level, and tuning parameter regime (\$P < P\_c\$, etc.).

---

## ⚙️ Hamiltonian and Dispersion

Work with:

$$
H(\mathbf{k}) = A(k_x \sigma_x + k_y \sigma_y) + M(\mathbf{k}) \sigma_z
\quad \text{with} \quad M(\mathbf{k}) = M_0 - B(k_x^2 + k_y^2)
$$

Set:

* \$A = 1\$, \$B = 1\$
* Plot along \$k\_x\$, fixing \$k\_y = 0\$
* Dispersion: \$E\_\pm(k) = \pm \sqrt{A^2 k^2 + M(k)^2}\$

---

## 🎨 Visual Design

### Color Palette

* **Conduction band**: red
* **Valence band**: blue
* **Inverted region** (for \$P > P\_c\$): purple overlay
* **Fermi level**: black horizontal line at \$E=0\$
* **Parity labels**: `$+$` for even, `$-$` for odd
* **\$\mathbb{Z}\_2\$ label**: Top left in each panel

### Key Graphical Elements

* Smooth lobes or parabolas (not shaded 3D cones)
* Bands clearly separated (except at critical point)
* Dotted arrows showing band evolution across panels
* Horizontal label bar: `"Tuning SOC strength"` with arrow

---

## 🖼️ Panel (a): Trivial Insulator (\$\mathbb{Z}\_2 = 0\$)

* **\$M\_0 = +1\$**, \$P < P\_c\$
* CBM above, VBM below, parity: CBM \$-\$, VBM \$+\$
* No overlap, direct bandgap

**Annotations**:

* \$\mathbb{Z}\_2 = 0\$
* Parity labels: `+` (VBM), `−` (CBM)
* “Normal Insulator”
* “\$P < P\_c\$” under subplot

---

## 🖼️ Panel (b): Dirac Semimetal (\$P = P\_c\$)

* **\$M\_0 = 0\$**, \$P = P\_c\$
* Bands touch at \$k=0\$, no gap
* Dirac cone: critical point

**Annotations**:

* Label Dirac point at \$k=0\$
* “Gapless”, “\$P = P\_c\$”
* \$\mathbb{Z}\_2\$ undefined or gray
* Mark conical shape, parity degeneracy

---

## 🖼️ Panel (c): Topological Insulator (\$\mathbb{Z}\_2 = 1\$)

* **\$M\_0 = -1\$**, \$P > P\_c\$
* Inverted band structure: red (original CB) is now below blue (original VB) at \$k=0\$
* Parity swapped: CBM has \$+\$, VBM has \$-\$
* Inversion region near \$k=0\$ should be highlighted

**Annotations**:

* \$\mathbb{Z}\_2 = 1\$
* “Band Inversion”
* “Topological Insulator”
* “\$P > P\_c\$” under subplot

---

## 🧑‍💻 Updated Python Code (Flat 2D, Parity Annotated)

```python
import numpy as np
import matplotlib.pyplot as plt

A, B = 1, 1
k = np.linspace(-1.5, 1.5, 500)
M_vals = [1.0, 0.0, -1.0]
titles = ['(a) Normal Insulator', '(b) Dirac Semimetal', '(c) Topological Insulator']
z2_labels = ['Z₂ = 0', '', 'Z₂ = 1']
parity_labels = [('+', '-'), ('', ''), ('-', '+')]
P_labels = ['P < Pₚ', 'P = Pₚ', 'P > Pₚ']

fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

for i, M0 in enumerate(M_vals):
    M_k = M0 - B * k**2
    E_plus = np.sqrt((A * k)**2 + M_k**2)
    E_minus = -E_plus

    ax = axs[i]
    ax.plot(k, E_plus, 'red', linewidth=2)
    ax.plot(k, E_minus, 'blue', linewidth=2)

    if M0 < 0:
        inv = np.where(M_k**2 < (A * k)**2)[0]
        ax.fill_between(k[inv], E_minus[inv], E_plus[inv], color='purple', alpha=0.2)

    # Fermi level
    ax.axhline(0, color='black', linestyle='--', linewidth=1)

    # Parity labels
    if parity_labels[i]:
        ax.text(0.1, E_plus[0] + 0.3, parity_labels[i][1], fontsize=16, color='red')
        ax.text(0.1, E_minus[0] - 0.6, parity_labels[i][0], fontsize=16, color='blue')

    ax.set_title(titles[i], fontsize=12)
    ax.text(0, 2.2, z2_labels[i], ha='center', fontsize=14, fontweight='bold')
    ax.text(0, -2.3, P_labels[i], ha='center', fontsize=12)
    ax.set_xlabel('$k$', fontsize=12)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_xticks([])
    ax.set_yticks([])

axs[0].set_ylabel('Energy $E(k)$', fontsize=12)

# SOC tuning arrow
fig.text(0.5, 0.03, 'Tuning SOC Strength', ha='center', fontsize=14)
fig.annotate('', xy=(0.75, 0.04), xytext=(0.25, 0.04),
             xycoords='figure fraction', arrowprops=dict(arrowstyle='->', lw=2))

plt.tight_layout()
plt.show()
```

---

## ✅ Summary Table

| Panel | \$P\$ Regime | \$M\_0\$ | \$\mathbb{Z}\_2\$ | Parity Swap | Notes                                   |
| ----- | ------------ | -------- | ----------------- | ----------- | --------------------------------------- |
| (a)   | \$P < P\_c\$ | \$+1\$   | 0                 | No          | Normal insulator, gap, no edge states   |
| (b)   | \$P = P\_c\$ | \$0\$    | —                 | Swapping    | Dirac cone, gapless                     |
| (c)   | \$P > P\_c\$ | \$-1\$   | 1                 | Yes         | Inverted bands, topological edge states |

---

Let me know if you want a vectorized SVG export or LaTeX TikZ version.
