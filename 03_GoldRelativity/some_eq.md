Here's a fully self-contained explanation, with all key steps expanded inline:

---

Gold absorbs blue light (∼2.4 eV) because the **energy gap between its 5d and 6s orbitals is reduced by relativistic effects**, bringing this electronic transition into the visible spectrum. The mechanism involves **how relativity changes orbital energies** by altering the wavefunction behavior near the nucleus.

### Step 1: Electrons are wavefunctions

Electrons in atoms are not tiny particles moving in orbits—they are described by **wavefunctions** governed by the **Schrödinger equation**:

$$
\left[ -\frac{\hbar^2}{2m} \nabla^2 - \frac{Ze^2}{r} \right] \psi = E \psi
$$

* The **first term**, $-\frac{\hbar^2}{2m} \nabla^2$, is the **kinetic energy operator**. It penalizes sharp changes in the wavefunction—i.e., localization. The mass $m$ appears in the denominator, so **higher mass reduces this kinetic penalty**.
* The **second term**, $-\frac{Ze^2}{r}$, is the **Coulomb potential energy**: the attractive force between the negatively charged electron and the positively charged nucleus. Smaller $r$ (closer to the nucleus) means **stronger binding**.

So electrons try to localize near the nucleus to benefit from lower potential energy—but localization increases kinetic energy due to the **uncertainty principle**:

$$
\Delta x \cdot \Delta p \gtrsim \frac{\hbar}{2}
$$

A small $\Delta x$ (tight localization) leads to large $\Delta p$, i.e., high momentum components.

---

### Step 2: High momentum ⇒ high velocity ⇒ relativistic energy corrections

For inner orbitals (like 1s, 2s, or 6s in gold), the wavefunction is strongly peaked near $r = 0$, so the electron is highly localized. This implies **large momentum components**. When these momentum scales correspond to velocities approaching a significant fraction of the **speed of light $c$**, we must use **relativistic mechanics**.

The total energy of a relativistic particle is:

$$
E = \frac{m_0 c^2}{\sqrt{1 - \frac{v^2}{c^2}}}
$$

where $m_0$ is the invariant rest mass. At high velocities, the **total energy increases dramatically** above the rest energy $m_0 c^2$, leading to significant **relativistic energy corrections** in the quantum mechanical description.

---

### Step 3: Why relativistic energy corrections lead to orbital contraction

In the relativistic quantum mechanical description (the **Dirac equation**), the kinetic energy operator becomes more complex than the simple $\frac{p^2}{2m}$ form. The relativistic corrections modify how the kinetic energy depends on momentum, effectively **reducing the kinetic energy penalty** for high-momentum (highly localized) wavefunctions.

This means:

* Sharp wavefunction curvature (tight localization) costs **less kinetic energy** in the relativistic regime,
* So the electron **can afford to be even more localized** near the nucleus,
* The result is a **contracted orbital** with **lower total energy** (stronger binding).

In physical terms: relativistic corrections reduce the kinetic energy cost of localization = easier to bind close to the nucleus = more energy gained from the Coulomb potential.

This is especially true for **s-orbitals**, because:

* They have zero angular momentum,
* They penetrate right through the center ($r = 0$),
* So they “see” the full nuclear charge and gain the most from this relativistic effect.

---

### Step 4: Effect on gold's 5d → 6s transition

* The **6s orbital contracts** and its energy drops significantly due to relativistic energy corrections.
* The **5d orbitals**, which have angular momentum and are repelled from the nucleus by the centrifugal barrier, are **less affected**.
* This **reduces the energy gap** between 5d and 6s to about **2.4 eV**.
* This energy corresponds to **blue light**, which gold thus **absorbs**.
* The reflected spectrum is missing blue and skewed toward **red/yellow**, giving gold its **distinctive color**.

---

### Summary:

* **High nuclear charge (Z = 79)** pulls inner electrons close, forcing wavefunction localization.
* Localization means high momentum ⇒ high velocity ⇒ **relativistic energy corrections**.
* Relativistic corrections reduce kinetic energy cost of localization ⇒ **s-orbitals contract**.
* Contracted orbitals gain more binding energy from the **Coulomb potential** $-\frac{Ze^2}{r}$,
* This shifts transition energies—specifically **5d → 6s**—into the visible range (∼2.4 eV),
* Hence, gold **absorbs blue** and reflects red/yellow: a visible signature of **relativistic quantum mechanics**.
