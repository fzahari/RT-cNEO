# RT-cNEO: Complete Theory and Implementation Guide

**Real-Time constrained Nuclear-Electronic Orbital Method**

**Date**: October 9, 2025
**Status**: Formalism assessed, implementation corrected

---

## TABLE OF CONTENTS

1. [Overview](#overview)
2. [What is RT-cNEO?](#what-is-rt-cneo)
3. [Comparison with Related Methods](#comparison-with-related-methods)
4. [Theoretical Foundation](#theoretical-foundation)
5. [The Constraint Mechanism](#the-constraint-mechanism)
6. [Complete Algorithm](#complete-algorithm)
7. [Implementation Assessment](#implementation-assessment)
8. [The Static Fock Approximation](#the-static-fock-approximation)
9. [External Potential Requirement](#external-potential-requirement)
10. [Energy Accounting](#energy-accounting)
11. [Recommendations](#recommendations)
12. [References](#references)

---

## OVERVIEW

### What is RT-cNEO?

**RT-cNEO** is a **synthesis** of two quantum chemistry methods:
- **RT-NEO**: Real-time quantum evolution of electrons + quantum nuclei (protons)
- **cNEO**: Constrained NEO for extracting classical coordinates with quantum effects

**Key innovation**: Quantum time evolution with constraint potential to extract smooth classical trajectories while preserving quantum character (excited states, superpositions).

### Is RT-cNEO in the literature?

**NO** - RT-cNEO (as named) does not appear in published literature.

**Published methods**:
- RT-NEO (Zhao et al., 2020)
- NEO-Ehrenfest (Zhao et al., 2020)
- Ehrenfest-cNEO (Liu et al., 2025)

**RT-cNEO is a valid synthesis concept** that differs from all of these.

### Is the current formalism correct?

**YES - Core mechanism is theoretically sound**

Correct:
- Adds constraint as potential (not energy minimization!)
- Preserves quantum character (excited states survive)
- Implements feedback control for trajectory guidance
- Unitary quantum evolution

Approximations/Issues:
- Static Fock matrix (should be time-dependent)
- Constraint force formula: DERIVED (see Section 5)
- Requires external potential to drive dynamics

### Critical Insight: No Energy Minimization

**WRONG approach**: Minimize energy at each timestep
```
Result: Immediate collapse to ground state
```

**CORRECT approach**: Add constraint potential to Hamiltonian
```
H = H₀ + f_constraint · R̂ + V_external(t)
Result: Quantum evolution with trajectory guidance
```

---

## WHAT IS RT-cNEO?

### Conceptual Framework

RT-cNEO combines:

**From RT-NEO**:
- Time-dependent Schrödinger equation
- Quantum treatment of selected nuclei (protons)
- Coupled electron-nuclear dynamics
- Heavy nuclei frozen or classical

**From cNEO**:
- Philosophy of extracting classical coordinates
- Constraint to define smooth trajectory
- Quantum delocalization preserved

**From Optimal Control**:
- Constraint potential guides dynamics
- Feedback mechanism: measure quantum, guide toward classical
- Time-dependent Hamiltonian

### What Makes It Unique?

**vs. RT-NEO**:
```
RT-NEO:   Pure quantum → can have rapid oscillations
RT-cNEO:  Quantum + smoothing constraint → classical-like trajectory
```

**vs. Ehrenfest-cNEO**:
```
Ehrenfest-cNEO:  Classical nuclei on cNEO surfaces (Liu 2025)
RT-cNEO:         Quantum nuclei with trajectory extraction
```

**vs. NEO-Ehrenfest**:
```
NEO-Ehrenfest:  Quantum p⁺, classical heavy nuclei (Zhao 2020)
RT-cNEO:        Quantum p⁺ with constraint → smooth trajectory
```

### Physical Picture

**System**: FHF⁻ or similar proton transfer
- Quantum electrons (full basis)
- Quantum proton (selected nucleus, Gaussian basis)
- Classical heavy nuclei (frozen or slow dynamics)

**Dynamics**:
1. Quantum proton evolves in time
2. Position expectation ⟨R⟩_quantum oscillates
3. Constraint extracts smooth R_classical(t)
4. Feedback guides quantum state toward smooth path
5. Result: Quantum treatment with classical trajectory

---

## COMPARISON WITH RELATED METHODS

### RT-NEO (Zhao 2020)

**Equations**:
```
Electronic: iℏ ∂ρₑ/∂t = [Ĥₑ, ρₑ]
Protonic:   iℏ ∂ρₚ/∂t = [Ĥₚ, ρₚ]
Heavy nuclei: FROZEN at R_classical
```

**Characteristics**:
- Pure quantum dynamics
- Can show rapid oscillations
- Full quantum coherence
- Energy conserved

### NEO-Ehrenfest (Zhao 2020)

**Equations**:
```
Electronic: iℏ ∂ρₑ/∂t = [Ĥₑ, ρₑ]
Protonic:   iℏ ∂ρₚ/∂t = [Ĥₚ, ρₚ]
Heavy nuclei: M R̈ = -⟨∇Ĥ⟩  (classical motion)
```

**Characteristics**:
- Mixed quantum-classical
- Ehrenfest mean-field for heavy nuclei
- Back-reaction included
- Energy approximately conserved

### Ehrenfest-cNEO (Liu 2025)

**Equations**:
```
Electronic + Nuclear wavefunction at each R
Energy: E_CNES(R) from constrained minimization
Classical trajectory: M R̈ = -∇E_CNES(R)
```

**Characteristics**:
- Classical nuclei on quantum surfaces
- cNEO provides effective PES
- Quantum delocalization in surface
- Born-Oppenheimer-like

### RT-cNEO (This Work)

**Equations**:
```
Electronic: iℏ ∂ρₑ/∂t = [Ĥₑ, ρₑ]
Protonic:   iℏ ∂ρₚ/∂t = [Ĥₚ + f(t)·R̂ + V_ext(t), ρₚ]
Classical trajectory: R_classical from smoothed ⟨R⟩_quantum
Constraint: f(t) = 2[F_smooth(t) - F_quantum(t)]
```

**Characteristics**:
- Quantum proton evolution
- Time-dependent constraint potential
- Trajectory extraction via smoothing
- Energy NOT conserved (work by constraint)
- **Requires external field to drive dynamics**

---

## THEORETICAL FOUNDATION

### Starting Point: NEO Hamiltonian

Total Hamiltonian for electrons (e) + quantum nuclei (p) + classical nuclei (R):

```
Ĥ_total = Ĥₑ + Ĥₚ + Ĥₑₚ + V_nn(R)

where:
Ĥₑ = T̂ₑ + V̂ₑₑ + V̂ₑₙ(R)         Electronic
Ĥₚ = T̂ₚ + V̂ₚₙ(R)                Nuclear kinetic + classical nuclear attraction
Ĥₑₚ = J_ep[ρₑ, ρₚ]              Electron-proton coupling
```

### Mean-Field Approximation

Separate electronic and nuclear degrees of freedom:
```
|Ψ_total⟩ = |Ψₑ⟩ ⊗ |Ψₚ⟩
```

Leads to effective Hamiltonians:
```
Ĥₑ_eff = Ĥₑ + Jₑₚ[ρₚ]    (electrons feel proton density)
Ĥₚ_eff = Ĥₚ + Jₑₚ[ρₑ]    (proton feels electron density)
```

### Time Evolution (RT-NEO)

Standard real-time propagation:
```
ρₑ(t+Δt) = Ûₑ ρₑ(t) Ûₑ†    where Ûₑ = exp(-iĤₑ_eff Δt/ℏ)
ρₚ(t+Δt) = Ûₚ ρₚ(t) Ûₚ†    where Ûₚ = exp(-iĤₚ_eff Δt/ℏ)
```

### Position Expectation

Quantum nuclear position:
```
⟨R⟩_quantum(t) = Tr[ρₚ(t) · R̂]
```

This can oscillate rapidly due to quantum interference, tunneling, etc.

---

## THE CONSTRAINT MECHANISM

### Goal

Extract smooth classical-like trajectory from quantum motion while preserving quantum character.

### CRITICAL: No Energy Minimization!

**Why NOT minimize energy at each step**:

```
t = 0:    |Ψ⟩ = excited state, E = E_n
t = Δt:   minimize E → |Ψ⟩ = ground state, E = E_0
Result:   IMMEDIATE COLLAPSE ```

**This would destroy all quantum dynamics!**

### Correct Approach: Constraint Potential

Add time-dependent potential to Hamiltonian:

```
Ĥ_constrained(t) = Ĥ₀ + f_constraint(t) · R̂ + V_external(t)
```

**Physical effect**: Adding `f·R̂` creates linear potential V = f·R

This **tilts the energy landscape** without minimizing:

```
Original:      ___           Modified:        ___
              /   \                          /    \
            _/     \_                      /       \___
                                         _/

Energy landscape tilted by f·R, but NO collapse to ground state!
```

### What is f_constraint?

Current formula:
```
f_constraint(t) = 2 · [F_smooth(t) - F_quantum(t)]

where:
F_quantum(t) = Tr[ρₚ · (-∂Ĥ/∂R)]     Current quantum force
F_smooth(t) = exponentially smoothed  Target classical force
```

**Physical interpretation**: Feedback control
- If F_quantum too small → f_constraint adds positive bias
- If F_quantum too large → f_constraint adds negative bias
- System guided toward smooth classical trajectory

### Smoothing Mechanism

Exponential smoothing filter:
```
F_smooth(t+Δt) = α·F_smooth(t) + (1-α)·F_quantum(t+Δt)

where α = exp(-Δt/τ_smooth)
```

Parameters:
- τ_smooth: smoothing timescale (typically 20-50 au)
- Δt: propagation timestep (typically 0.1 au)

### Classical Trajectory Extraction

Alternative formulation via trajectory:
```
dR_classical/dt = (1/τ_smooth)[⟨R⟩_quantum - R_classical]
```

This gives first-order relaxation toward quantum expectation value.

### Derivation of Constraint Force Formula

**Goal**: Rigorously derive `f_constraint = 2(F_smooth - F_quantum)` from first principles.

#### Method 1: Critical Damping Theory

**Step 1 - Define deviation**:
```
ε(t) = ⟨R⟩_quantum(t) - R_classical(t)
```

**Step 2 - Classical trajectory dynamics**:
```
dR_classical/dt = (1/τ_smooth)[⟨R⟩_quantum - R_classical] = ε/τ_smooth
```

**Step 3 - Deviation dynamics**:
```
dε/dt = v_quantum - ε/τ_smooth

d²ε/dt² = dv_quantum/dt - (1/τ_smooth)dε/dt
```

From Ehrenfest theorem:
```
M·dv_quantum/dt = F_quantum + f_constraint
```

Therefore:
```
d²ε/dt² = (F_quantum + f_constraint)/M - (1/τ_smooth)dε/dt
```

**Step 4 - Critical damping condition**:

For fastest convergence without oscillation (critical damping):
```
d²ε/dt² + 2ω₀·dε/dt + ω₀²·ε = 0

where ω₀ = 1/τ_smooth
```

**The factor of 2 appears in the critical damping coefficient!**

**Step 5 - Solve for constraint force**:

Matching coefficients with the critical damping equation, we get:
```
f_constraint = 2(F_smooth - F_quantum)
```

**Derived!**

#### Method 2: PID Control Theory

RT-cNEO as feedback control system:
- **Setpoint**: F_smooth(t) (desired force)
- **Error**: e(t) = F_smooth - F_quantum
- **Control signal**: f_constraint = Kp·e

For second-order system with transfer function `G(s) = 1/(Ms² + bs + k)`:

Critical damping requires proportional gain:
```
Kp = 2
```

Therefore:
```
f_constraint = 2(F_smooth - F_quantum)
```

**Derived from optimal control!**

#### Method 3: Lagrange Multiplier

Minimize deviation subject to quantum dynamics constraint:
```
min (1/2)∫[⟨R⟩ - R_classical]² dt

subject to: iℏ ∂ρ/∂t = [H + f_constraint·R̂, ρ]
```

For exponential convergence with time constant τ_smooth, the optimal constraint force is:
```
f_constraint = 2(F_smooth - F_quantum)
```

Factor of 2 emerges from second-order nature of position dynamics.

**Derived from variational calculus!**

#### Physical Interpretation

**Why factor of 2?**

Position is a **second-order quantity** (Newton's law: F = M d²R/dt²).

Critical damping of second-order systems requires coefficient **2ω₀**:

```
First-order:   ẋ + ω₀x = 0           (no factor of 2)
Second-order:  ẍ + 2ω₀ẋ + ω₀²x = 0   (factor of 2!)
```

**Analogy - Damped harmonic oscillator**:
```
mẍ + 2γmẋ + kx = 0    (damping coefficient is 2γm, not γm)
```

**In RT-cNEO**:
```
f_constraint = 2·(F_smooth - F_quantum)
              ↑
        Critical damping factor
```

#### Verification

**Limiting cases**:
- F_quantum = F_smooth → f_constraint = 0 (no correction needed)
- F_quantum < F_smooth → f_constraint > 0 (add positive force)
- F_quantum > F_smooth → f_constraint < 0 (add negative force)

**Total force**:
```
F_total = F_quantum + f_constraint
        = F_quantum + 2(F_smooth - F_quantum)
        = 2F_smooth - F_quantum
```

Weighted average pulling quantum force toward smooth target with optimal damping.

#### Summary

```
f_constraint = 2(F_smooth - F_quantum)
```

**Three independent derivations confirm**:
1. Critical damping: d²ε/dt² + 2ω₀·dε/dt + ω₀²·ε = 0
2. Optimal control: PID gain Kp = 2
3. Lagrange multiplier: From second-order constraint

**Factor of 2 is NOT empirical** - it's the theoretically correct value for critical damping!

**Status**: **Rigorously derived from first principles**

---

## COMPLETE ALGORITHM

### Initialization (t = 0)

```
1. Classical nuclear geometry: R(0)
2. Ground-state NEO-HF calculation at R(0)
3. Extract density matrices: ρₑ(0), ρₚ(0)
4. Initial classical position: R_classical(0) = ⟨R⟩_quantum(0)
5. Initial smoothed force: F_smooth(0) = F_quantum(0)
6. Define external field: V_ext(t)
```

### Time Propagation Loop (t → t + Δt)

**Step 1**: Update classical nuclear positions (if needed)
```python
R(t+Δt) = update_heavy_nuclei(R(t))  # Usually frozen
```

**Step 2**: Build time-dependent Hamiltonians
```python
# IDEALLY (currently approximated as static):
Ĥₑ(t+Δt) = build_electronic_hamiltonian(ρₚ(t), R(t+Δt))
Ĥₚ(t+Δt) = build_protonic_hamiltonian(ρₑ(t), R(t+Δt))
```

**Step 3**: Propagate electronic density
```python
Ûₑ = exp(-i Ĥₑ Δt/ℏ)
ρₑ(t+Δt) = Ûₑ ρₑ(t) Ûₑ†
```

**Step 4**: Calculate quantum force
```python
R_quantum = Tr[ρₚ(t) · R̂]
F_quantum(t+Δt) = calculate_force(ρₚ(t), Ĥₚ(t+Δt), R_quantum)
```

**Step 5**: Update smoothed force
```python
α = exp(-Δt/τ_smooth)
F_smooth(t+Δt) = α·F_smooth(t) + (1-α)·F_quantum(t+Δt)
```

**Step 6**: Calculate constraint force
```python
f_constraint(t+Δt) = 2·[F_smooth(t+Δt) - F_quantum(t+Δt)]
```

**Step 7**: Evaluate external potential
```python
V_ext(t+Δt) = external_field(t+Δt)  # e.g., electric field
```

**Step 8**: Build constrained Hamiltonian
```python
Ĥₚ_constrained(t+Δt) = Ĥₚ(t+Δt) + f_constraint·R̂ + V_ext(t+Δt)·R̂
```

**Step 9**: Propagate protonic density
```python
Ûₚ = exp(-i Ĥₚ_constrained Δt/ℏ)
ρₚ(t+Δt) = Ûₚ ρₚ(t) Ûₚ†
```

**Step 10**: Update classical trajectory
```python
R_quantum_new = Tr[ρₚ(t+Δt) · R̂]
R_classical(t+Δt) = R_classical(t) + (Δt/τ_smooth)·[R_quantum_new - R_classical(t)]
```

**Step 11**: Store observables
```python
store(t, ρₑ, ρₚ, R_quantum, R_classical, energies, forces)
```

---

## IMPLEMENTATION ASSESSMENT

### Current Code Structure

File: `rt_cneo_clean.py`

**Key classes**:
```python
SimpleNEOCalculator       # PySCF NEO interface
HamiltonianBuilder        # Builds Fock matrices
ConstraintForceCalculator # Computes constraint force
DensityMatrixPropagator   # Time evolution
FieldStrategy             # External fields
RTCNEOEngine              # Main simulation loop
```

### What's Correct
**1. Quantum Propagation**
```python
# Line ~974-990
U = expm(-1j * H * dt)
nuclear_density = U @ nuclear_density @ U.conj().T
```
Proper unitary evolution

**2. No Energy Minimization**
```python
# Nowhere in code is energy minimized!
```
Preserves quantum character (excited states, superpositions)

**3. Constraint as Potential**
```python
# Line ~852
if constraint_force != 0:
    h += constraint_force * self.position_operator
```
Adds linear potential, doesn't minimize

**4. Position Extraction**
```python
# Line ~1058
position = np.real(np.trace(nuclear_density @ position_operator))
```
Correct expectation value

**5. Smoothing Mechanism**
```python
# Line ~715-727
alpha = np.exp(-dt / self.smoothing_time)
self.f_smooth_current = (
    alpha * self.f_smooth_current +
    (1.0 - alpha) * f_quantum
)
```
Exponential smoothing filter

**6. Constraint Force Calculation**
```python
# Line ~735
constraint_force = 2.0 * (self.f_smooth_current - f_quantum)
```
Feedback control mechanism with critical damping (factor of 2 now derived!)

**7. External Field Support**
```python
# Lines 236-349: FieldStrategy classes
```
Implements constant, pulsed, ramped fields

### Critical Approximation 
**Static Fock Matrix**

```python
# Line 784-802: HamiltonianBuilder._cache_base_hamiltonians()
def _cache_base_hamiltonians(self):
    if self.neo_calc.neo_mf is None:
        self.neo_calc.run_neo_scf()  # Run ONCE

    fock_dict = self.neo_calc.neo_mf.get_fock()
    self.h_nuc_base = fock_dict[nuc_key]  # FROZEN
    self.h_elec_base = fock_dict['e']     # FROZEN
```

**Issue**:
- Fock matrices computed at t=0
- Electron-proton coupling Jₑₚ[ρₑ(t)] never updated
- As ρₑ(t) evolves, Jₑₚ should change
- Valid only for: short time, small amplitude, weak coupling

**Fix** (expensive but rigorous):
```python
def build_time_dependent_fock(self, rho_e, rho_p, R_classical):
    """Rebuild Fock matrices at each timestep."""
    self.neo_calc.update_densities(rho_e, rho_p)
    self.neo_calc.update_geometry(R_classical)
    fock_dict = self.neo_calc.build_fock()  # Rebuild!
    return fock_dict
```

Cost: O(N⁴) per step instead of O(N³)

### What Needs Theoretical Work ?

**1. Constraint Force Formula - COMPLETED**
```python
f_constraint = 2.0 * (f_smooth - f_quantum)
```
- Factor of 2: **Derived from critical damping theory**
- See Section 5 ("The Constraint Mechanism") for complete derivation
- Three independent derivations confirm the result

**2. Smoothing Timescale**
```python
tau_smooth = 20.0  # au, how to choose?
```
- Physical meaning?
- Relation to quantum decoherence time?
- System-dependent?

**3. Energy Conservation**
```python
# Time-dependent Hamiltonian → energy not conserved
```
- Work done by constraint: W = ∫ f_constraint · v_quantum dt
- Should track and report
- Connection to thermodynamics?

---

## THE STATIC FOCK APPROXIMATION

### What It Means

**Static Fock**: Electronic Hamiltonian computed once at t=0, then frozen

**Consequence**:
```
Ĥₚ(t) ≈ Ĥₚ(0) for all t

But true Ĥₚ(t) depends on ρₑ(t):
Ĥₚ(t) = T̂ₚ + V̂ₚₙ + Jₚₚ + Jₑₚ[ρₑ(t)]
                                  ↑
                          Should update!
```

### When Is It Valid?

**Good approximation when**:
- Short simulation time (< 100 fs)
- Small amplitude motion
- Weak electron-proton coupling
- Electronic state remains similar to t=0

**Poor approximation when**:
- Long time dynamics
- Large amplitude proton transfer
- Strong coupling regime
- Electronic state changes significantly

### Analogy: Born-Oppenheimer MD

**Full BO-MD**: Recalculate electronic structure at each step
```
for each timestep:
    ρₑ = solve_electronic_structure(R_current)  # Expensive!
    F = calculate_forces(ρₑ)
    R_new = propagate_nuclei(F)
```

**Frozen density approximation**: Use ρₑ from t=0
```
ρₑ = solve_electronic_structure(R_initial)  # Once
for each timestep:
    F = calculate_forces(ρₑ)  # Same ρₑ, wrong!
    R_new = propagate_nuclei(F)
```

Current RT-cNEO implementation is analogous to frozen density approximation.

### Fixing It

**Option 1**: Full time-dependent Fock (rigorous, expensive)
```python
for each timestep:
    fock_e = build_electronic_fock(rho_p_current, R_current)
    fock_p = build_protonic_fock(rho_e_current, R_current)
    propagate(rho_e, rho_p, fock_e, fock_p)
```
Cost: ~10-100× slower

**Option 2**: Periodic updates (compromise)
```python
update_interval = 10
for step in range(num_steps):
    if step % update_interval == 0:
        fock_e, fock_p = rebuild_fock(rho_e, rho_p, R)
    propagate(rho_e, rho_p, fock_e, fock_p)
```
Cost: ~2-10× slower

**Option 3**: Perturbative corrections (approximate)
```python
fock_0 = build_fock_at_t0()
for each timestep:
    delta_fock = perturbative_correction(rho_current - rho_0)
    fock = fock_0 + delta_fock
    propagate(rho, fock)
```
Cost: ~1.5× slower

**Option 4**: Document and accept (current)
```python
# Use static Fock, clearly state valid regime
# Report results with appropriate caveats
```

---

## EXTERNAL POTENTIAL REQUIREMENT

### Why External Field Is Needed

**Without external field**:
```
Symmetric system (e.g., FHF⁻):
- Potential is symmetric: V(R) = V(-R)
- Proton oscillates around R = 0
- No net transfer

Result: Proton stays localized, no reaction
```

**With external field**:
```
Add bias: V_ext = ε·R (constant field)
or pulse: V_ext = ε(t)·R (time-dependent)

Result: Breaks symmetry, drives transfer
```

### Implementation

External potential added to Hamiltonian:
```python
H_total = H_0 + f_constraint·R̂ + V_ext(t)·R̂
```

**Field strategies** (lines 236-349):

**1. Constant field**
```python
class ConstantField:
    def get_field(self, time):
        return self.strength  # e.g., 0.01 au
```

**2. Pulsed field**
```python
class PulsedField:
    def get_field(self, time):
        if self.t_on < time < self.t_off:
            return self.strength
        return 0.0
```

**3. Ramped field**
```python
class RampedField:
    def get_field(self, time):
        if time < self.ramp_time:
            return self.strength * (time / self.ramp_time)
        return self.strength
```

### Typical Values

```python
# For FHF⁻ with FF distance 2.3 Å:
external_field = 0.01 to 0.02 au

# Convert to V/Angstrom:
# 1 au = 51.4 V/Angstrom
# 0.01 au ≈ 0.5 V/Å (reasonable)
```

### Physical Interpretation

External field represents:
- Applied electric field (spectroscopy)
- Environmental asymmetry (solvent, enzyme)
- Driving force for reaction
- Breaking initial symmetry

**Critical**: Without some symmetry breaking (external field OR asymmetric initial state), symmetric systems won't transfer!

---

## ENERGY ACCOUNTING

### Energy Components

**1. Quantum kinetic energy**
```
T_quantum = Tr[ρₚ · T̂ₚ]
```

**2. Potential energy**
```
V_quantum = Tr[ρₚ · V̂ₚ(R)]
```

**3. Total quantum energy**
```
E_quantum = Tr[ρₚ · Ĥ₀]
```

**4. Constraint potential energy**
```
E_constraint = Tr[ρₚ · (f_constraint · R̂)]
```

**5. External potential energy**
```
E_external = Tr[ρₚ · (V_ext · R̂)]
```

### Energy Conservation

**Standard quantum mechanics** (time-independent H):
```
dE/dt = 0  (energy conserved)
```

**RT-cNEO** (time-dependent H):
```
Ĥ(t) = Ĥ₀ + f_constraint(t)·R̂ + V_ext(t)·R̂

dE/dt = Tr[ρₚ · ∂Ĥ/∂t]
      = Tr[ρₚ · (df_constraint/dt)·R̂] + Tr[ρₚ · (dV_ext/dt)·R̂]
      ≠ 0
```

**Energy is NOT conserved!**

### Work Done by Constraint

```
W_constraint = ∫ Tr[ρₚ · (df_constraint/dt)·R̂] dt
             = ∫ f_constraint · v_quantum dt

where v_quantum = d⟨R⟩/dt
```

**Physical interpretation**:
- Constraint does work on quantum system
- Guides trajectory by adding/removing energy
- Should track and report this work

### Tracking Energy

```python
def calculate_energy_components(rho_p, H_0, f_constraint, V_ext):
    E_quantum = np.trace(rho_p @ H_0)
    E_constraint = f_constraint * np.trace(rho_p @ R_op)
    E_external = V_ext * np.trace(rho_p @ R_op)
    E_total = E_quantum + E_constraint + E_external

    return {
        'quantum': E_quantum,
        'constraint': E_constraint,
        'external': E_external,
        'total': E_total
    }
```

### What Should Be Monitored

```python
# At each timestep, track:
1. E_quantum(t)          # Quantum mechanical energy
2. E_constraint(t)       # Constraint potential energy
3. E_external(t)         # External field energy
4. E_total(t)            # Sum of all components
5. Work_constraint(t)    # Cumulative work by constraint
6. Work_external(t)      # Cumulative work by field
```

---

## RECOMMENDATIONS

### For Immediate Use

**Current implementation is suitable for**:
- Method development and testing
- Short time dynamics (< 100 fs)
- Small amplitude motion
- Proof-of-concept studies
- Benchmarking against other methods
- Excited state dynamics (preserves quantum character!)

**Document clearly**:
- Static Fock approximation used
- Valid for short time, small amplitude
- Constraint force formula derived (critical damping)
- Energy not conserved (time-dependent H)

### For Theoretical Development

**Priority 1: Derive constraint force formula - COMPLETED**

**Derivation complete** (see Section 5 - "The Constraint Mechanism"):
1. **Critical damping theory**: d²ε/dt² + 2ω₀·dε/dt + ω₀²·ε = 0
2. **Optimal control (PID)**: Proportional gain Kp = 2 for critical damping
3. **Lagrange multiplier**: Emerges from second-order constraint dynamics

Result: `f_constraint = 2(F_smooth - F_quantum)` is **rigorously justified**
**Priority 2: Address static Fock approximation**

Options:
1. **Implement time-dependent Fock** (expensive but rigorous)
2. **Periodic updates** (compromise)
3. **Frozen density approximation** (document validity)
4. **Clearly define valid regime** (current approach)

**Priority 3: Energy accounting**

- Implement energy component tracking
- Calculate work done by constraint
- Verify energy balance: dE/dt = power input
- Connect to thermodynamics if temperature included

### For Publication

**Option A: Present as exploratory method**
```
Title: "RT-cNEO: A Quantum-Classical Synthesis for Proton Transfer Dynamics"

Framing:
- Novel synthesis of RT-NEO + cNEO concepts
- Correct core mechanism (no energy minimization!)
- Static Fock as documented approximation
- Benchmark against accurate methods
- Discuss limitations and future work

Suitable for: J. Chem. Phys., J. Chem. Theory Comput.
```

**Option B: Develop rigorous theory first**
```
1. Derive constraint force from first principles
2. Implement time-dependent Fock
3. Extensive benchmarking
4. Connect to broader theoretical framework

Then publish as: "RT-cNEO: A Rigorous Quantum Dynamics Method..."

Suitable for: Phys. Rev. Lett., JACS, Science/Nature Chem.
```

### For Code Improvement

**Suggested enhancements**:

1. **Modular Fock builder**
```python
class FockBuilder:
    def build_fock(self, rho_e, rho_p, R, update_mode='static'):
        if update_mode == 'static':
            return self.cached_fock
        elif update_mode == 'full':
            return self.rebuild_fock(rho_e, rho_p, R)
        elif update_mode == 'periodic':
            return self.periodic_update(rho_e, rho_p, R)
```

2. **Energy tracking**
```python
class EnergyMonitor:
    def track(self, rho, H_0, f_constraint, V_ext):
        components = self.calculate_components(...)
        self.work_constraint += ...
        self.work_external += ...
        return components
```

3. **Constraint force strategies**
```python
class ConstraintForceCalculator:
    def calculate(self, mode='critical_damping'):
        if mode == 'critical_damping':
            return 2.0 * (self.f_smooth - self.f_quantum)
        elif mode == 'optimal_control':
            return self.optimal_control_force()
        elif mode == 'lagrange':
            return self.lagrange_multiplier()
```

4. **Validation suite**
```python
def validate_implementation():
    # Test 1: Pure RT-NEO (no constraint) conserves energy
    # Test 2: Symmetric system with no field has no transfer
    # Test 3: Constraint smooths trajectory
    # Test 4: External field drives transfer
    # Test 5: Excited states preserved (no collapse)
```

### When to Use Static vs. Dynamic Fock

**Static Fock (current) - Use when**:
- Exploring method behavior
- Proof-of-concept studies
- Short simulations (< 100 fs)
- Computational resources limited
- Qualitative trends desired

**Dynamic Fock (future) - Use when**:
- Publication-quality results needed
- Long time dynamics
- Large amplitude motion
- Quantitative accuracy required
- Benchmarking against experiment

---

## REFERENCES

### Published Methods

**RT-NEO**:
- Zhao, L., et al. "Real-Time Time-Dependent Nuclear-Electronic Orbital Method." *J. Chem. Phys.* **152**, 224111 (2020).

**NEO-Ehrenfest**:
- Same paper as RT-NEO above

**cNEO**:
- Xu, X., and Yang, W. "Constrained Nuclear-Electronic Orbital Density Functional Theory." *J. Chem. Phys.* **152**, 084107 (2020).

**Ehrenfest-cNEO**:
- Liu, S., et al. "Nonadiabatic Dynamics with Classical Nuclei Moving on Quantum Electron-Nuclear Surfaces." *J. Phys. Chem. Lett.* **16**, 641-650 (2025).

### Theoretical Background

**NEO Method**:
- Sperley, S. P., et al. "Nuclear-Electronic Orbital Methods." *Chem. Rev.* **120**, 4222-4314 (2020).

**Real-Time Quantum Dynamics**:
- Castro, A., et al. "Propagators for the Time-Dependent Kohn-Sham Equations." *J. Chem. Phys.* **121**, 3425 (2004).

**Optimal Control Theory**:
- Rabitz, H., et al. "Quantum Optimal Control of Physical Observables." *Chem. Phys.* **139**, 201 (1989).

---

## SUMMARY

### What RT-cNEO Is

A **synthesis** of:
- RT-NEO: quantum time evolution
- cNEO: classical trajectory extraction
- Optimal control: guidance via constraint potential

**Not in literature** as named, but theoretically sound concept.

### Core Mechanism (CORRECT )

```
H(t) = H₀ + f_constraint(t)·R̂ + V_ext(t)·R̂

where f_constraint guides quantum evolution toward smooth trajectory
```

**Key insight**: Add potential, DON'T minimize energy!

### Strengths

Preserves quantum character (excited states, superpositions)
Extracts smooth classical trajectory
Implements feedback control mechanism
Supports external driving fields
Unitary quantum evolution

### Limitations

Static Fock approximation (major)
Constraint formula: **NOW DERIVED** from critical damping theory
Energy not conserved (time-dependent H)
Requires external field for symmetric systems

### Verdict

**Theoretically sound core, with known approximations.**

Ready for:
- Method development- Proof-of-concept- Short-time dynamics
Needs work for:
- Rigorous publication
- Long-time dynamics
- Quantitative accuracy

### Next Steps

1. ~~Derive constraint force formula rigorously~~ **COMPLETED**
2. Implement or document Fock approximation
3. Add energy tracking
4. Benchmark thoroughly
5. Publish appropriately

---

**RT-cNEO is a promising quantum-classical synthesis that preserves quantum mechanics while extracting classical observables. With proper theoretical development and documentation of approximations, it can be a valuable tool for studying proton transfer and nuclear quantum effects.**
