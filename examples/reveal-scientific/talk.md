---
metadata:
  - title:    "High-Order Numerical Methods for the Incompressible Navier-Stokes Equations"
  - subtitle: "Stability, Accuracy, and Scalability on Adaptive Meshes"
  - authors:
    - Alice Rossi
    - Bruno Mancini
    - Carol Zhang
  - authors_short:
    - A. Rossi
    - B. Mancini
    - C. Zhang
  - emails:
    - a.rossi@fluid.example.edu
    - b.mancini@fluid.example.edu
    - c.zhang@hpc.example.edu
  - affiliations:
    - Fluid Dynamics Laboratory, Example University
    - Fluid Dynamics Laboratory, Example University
    - High-Performance Computing Centre, Example Institute
  - affiliations_short:
    - FDL — Example University
    - HPC — Example Institute
  - date:             "ICFD 2026, April 4–6"
  - conference:       "International Conference on Fluid Dynamics"
  - conference_short: "ICFD 2026"
  - session:          "Session 4B — High-Order Methods"
  - max_time:         30
  - toc_depth:        2
---

---
reveal:
  theme:      moon
  transition: slide
---

# Motivation

## Background

### The Problem

#### $titlepage

$box
$style[width:100%;background:linear-gradient(135deg,#1a1a2e,#16213e);border-radius:12px;padding:5%]
$content[color:white;text-align:center;]{
$conference[display:block;font-size:90%;opacity:0.7;padding-bottom:2%]
$session[display:block;font-size:80%;opacity:0.6;padding-bottom:4%]
$title[display:block;font-size:160%;font-weight:bold;padding-bottom:2%]
$subtitle[display:block;font-size:100%;opacity:0.85;padding-bottom:4%]
$authors[display:block;font-size:105%]
$affiliations[display:block;font-size:80%;opacity:0.7;padding-top:1%]
$date[display:block;font-size:80%;opacity:0.6;padding-top:3%]
}
$endbox

$note
$content{
Good morning/afternoon.

Today I will present our recent work on high-order discretisations for
the incompressible Navier-Stokes equations, with a focus on adaptive
mesh refinement and parallel scalability.

This is joint work with Bruno Mancini (fluid dynamics) and Carol Zhang
(HPC implementation).

Talk is 25 minutes + 5 minutes Q&A.
}
$endnote

#### Why Incompressible Navier-Stokes?

The incompressible **Navier-Stokes equations** govern viscous fluid flows at
low Mach number — the regime relevant to

- aerodynamic drag at subsonic speeds
- cardiovascular and biomedical flows
- oceanic and atmospheric circulation (mesoscale)
- industrial mixing and heat exchangers

$$
\frac{\partial \mathbf{u}}{\partial t}
  + (\mathbf{u} \cdot \nabla)\mathbf{u}
  = -\nabla p + \nu \, \Delta \mathbf{u} + \mathbf{f},
\qquad \nabla \cdot \mathbf{u} = 0
$$

where $\mathbf{u}$ is velocity, $p$ is kinematic pressure, $\nu$ is
kinematic viscosity, and $\mathbf{f}$ is a body force.

$note
$content{
The key coupling is the pressure-velocity coupling enforced by the
divergence-free constraint.  This makes the problem a saddle-point system,
which requires inf-sup stable discretisations.

Most audience members work in this area — keep this slide short and move on.
}
$endnote

#### Challenges

$columns
$column[width:48%]
**Analytical challenges**

- Non-linear convective term $(\mathbf{u} \cdot \nabla)\mathbf{u}$
- Saddle-point pressure-velocity coupling
- Long-time stability at high Reynolds numbers
- Thin boundary layers (BL thickness $\sim Re^{-1/2}$)
$column[width:48%]
**Numerical challenges**

- Inf-sup stability (LBB condition)
- Conservation of energy and momentum
- Efficient pressure solvers
- Adaptive mesh refinement without accuracy loss
$endcolumns

$note
$content{
The LBB (Ladyzhenskaya-Babuška-Brezzi) condition is the key compatibility
condition between velocity and pressure approximation spaces.

Taylor-Hood elements (P2/P1) are the classic workaround; our approach uses
a different stabilisation strategy.
}
$endnote

## Prior Work

### State of the Art

#### Existing Approaches

$table
$caption{Overview of common velocity/pressure element pairs}
$content{
| Method            | Velocity order | Pressure order | LBB stable | Notes                  |
|-------------------|:--------------:|:--------------:|:----------:|------------------------|
| Taylor-Hood P2/P1 | 2              | 1              | ✓          | Classic workaround     |
| Mini element      | 1+bubble       | 1              | ✓          | Low cost, low accuracy |
| Scott-Vogelius    | $k$            | $k-1$          | ✓ (on special meshes) | Exact divergence-free |
| Discontinuous Galerkin (DG) | $k$ | $k$        | via penalisation | Flexible BCs    |
| **Ours** (HO-SEM) | $k$ (up to 8)  | $k-1$          | ✓          | Spectral accuracy      |
}
$endtable

$note
$content{
The table summarises what the audience probably already knows.
Our contribution (last row) is highlighted.

Key selling point: spectral accuracy means exponential convergence for
smooth problems — same accuracy with far fewer degrees of freedom.
}
$endnote

# Mathematical Framework

## Discretisation

### Spatial Discretisation

#### Spectral Element Method

We partition $\Omega$ into non-overlapping hexahedral elements $\{K_e\}$ and
approximate velocity in the space

$$
V_h^k = \left\{ \mathbf{v} \in [H^1(\Omega)]^d \;\middle|\;
         \mathbf{v}|_{K_e} \in \mathbb{Q}_k(K_e),\;
         \mathbf{v}|_{\partial\Omega_D} = 0 \right\}
$$

with $\mathbb{Q}_k$ denoting tensor-product polynomials of degree $\leq k$
on each element, and pressure in $Q_h^{k-1}$.

The **weak formulation**: find $(\mathbf{u}_h, p_h) \in V_h^k \times Q_h^{k-1}$ such that

$$
a(\mathbf{u}_h, \mathbf{v}) + b(\mathbf{v}, p_h)
  = (\mathbf{f}, \mathbf{v})_\Omega \quad \forall\, \mathbf{v} \in V_h^k
$$
$$
b(\mathbf{u}_h, q) = 0 \quad \forall\, q \in Q_h^{k-1}
$$

$note
$content{
The bilinear forms are the standard ones:
  a(u,v) = ν(∇u, ∇v) + c(u; u, v)   (viscous + convective)
  b(v, p) = −(p, ∇·v)                (pressure coupling)

The trilinear convective form c is skew-symmetrised for energy stability.
}
$endnote

#### Gauss-Lobatto-Legendre Quadrature

Integration uses **Gauss-Lobatto-Legendre (GLL)** points, which are the
roots of $(1-\xi^2)P'_{k}(\xi)$ plus $\pm 1$:

$$
\int_{-1}^{1} f(\xi)\,d\xi
  \approx \sum_{j=0}^{k} w_j \, f(\xi_j), \qquad
\xi_j \in [-1, 1],\; w_j > 0
$$

Properties:
- **Exact** for polynomials of degree $\leq 2k-1$
- Collocated with the interpolation nodes → diagonal mass matrix
- $\kappa(\mathbf{M}) = \mathcal{O}(1)$ — mesh-independent mass matrix conditioning

$note
$content{
The diagonal mass matrix is crucial for explicit time stepping — no system
to solve at each stage.

GLL quadrature is exact for our polynomial space, so no quadrature error
is introduced.
}
$endnote

### Temporal Discretisation

#### IMEX Runge-Kutta

We use a third-order **IMEX-RK** scheme (implicit viscous, explicit convective):

$$
\mathbf{u}^{(i)} = \mathbf{u}^n
  - \Delta t \sum_{j=1}^{i-1} \tilde{a}_{ij}\,
    \underbrace{(\mathbf{u}^{(j)} \cdot \nabla)\mathbf{u}^{(j)}}_{\text{explicit}}
  + \Delta t \sum_{j=1}^{i} a_{ij}\,
    \underbrace{\left(-\nabla p^{(j)} + \nu\Delta\mathbf{u}^{(j)}\right)}_{\text{implicit}}
$$

The stability region includes the imaginary axis, allowing $\Delta t \sim h/k^2$
rather than the CFL-constrained $\Delta t \sim h/k^2\,Re^{-1}$ of fully explicit schemes.

$box
$caption[color:#f39c12]{CFL condition (IMEX)}
$content[padding:0.8em]{
$$
\Delta t \leq C_{\mathrm{CFL}} \frac{h}{\|\mathbf{u}\|_\infty \, k^2}
$$
where $C_{\mathrm{CFL}} \approx 0.5$ and $h$ is the element diameter.
}
$endbox

$note
$content{
The IMEX scheme avoids the stiff viscous time step restriction (which scales
as 1/Re for explicit methods) while keeping the non-linear solve at the
explicit stage — so each stage only requires a linear saddle-point solve.

Third-order accuracy in time matches the spatial accuracy for moderate k.
}
$endnote

# Implementation

## Software

### Architecture

#### Code Structure

The solver is implemented in **Python** (driver layer) and **Fortran 2018**
(computational kernels), targeting hybrid MPI + OpenMP architectures.

```python
# Python driver: mesh → solver → output
from nssolver import Mesh, Solver, SolverConfig

cfg = SolverConfig(
    polynomial_order = 6,
    time_scheme      = "IMEX-RK3",
    dt               = 1e-4,
    t_end            = 10.0,
    output_interval  = 0.1,
)

mesh   = Mesh.from_gmsh("channel.msh", partitions=256)
solver = Solver(mesh, cfg)
solver.run()
solver.write_vtk("results/")
```

$note
$content{
The Python layer handles I/O, mesh partitioning, and time-loop control.
The Fortran kernels handle the inner loop: element assembly, GLL quadrature,
and sparse linear solves (via PETSc).

This keeps the high-level logic readable while keeping performance in Fortran.
}
$endnote

#### Fortran Kernel (GLL Assembly)

```fortran
subroutine assemble_local_stiffness(K_loc, dphidxi, w, nu, npt)
  implicit none
  integer,  intent(in)  :: npt
  real(8),  intent(in)  :: dphidxi(npt, npt), w(npt), nu
  real(8),  intent(out) :: K_loc(npt, npt)
  integer :: i, j, q

  K_loc = 0.0d0
  do q = 1, npt          ! GLL quadrature point
    do j = 1, npt        ! test function
      do i = 1, npt      ! trial function
        K_loc(i, j) = K_loc(i, j) &
          + nu * w(q) * dphidxi(q, i) * dphidxi(q, j)
      end do
    end do
  end do
end subroutine
```

$note
$content{
Tight inner loops like this are where Fortran shines over Python.
The loop order (q outer, i/j inner) is cache-friendly for column-major storage.

With -O2 and autovectorisation, this routine achieves ~85% of peak FLOP/s
on AMD EPYC 9654.
}
$endnote

# Results

## Convergence

### Accuracy

#### $h$-Convergence for Taylor-Couette Flow

Taylor-Couette flow (rotating cylinders) has an exact solution, enabling
rigorous convergence measurement.

$columns
$column[width:56%]
| $k$ | $N_{\rm elem}$ | $\|e_u\|_{L^2}$ | Rate |
|:---:|:--------------:|:---------------:|:----:|
| 2   | 64             | 2.41e-03        | —    |
| 2   | 256            | 6.02e-04        | 2.00 |
| 2   | 1024           | 1.51e-04        | 2.00 |
| 4   | 64             | 1.83e-06        | —    |
| 4   | 256            | 1.14e-07        | 4.00 |
| 6   | 16             | 8.71e-09        | —    |
| 6   | 64             | 1.36e-10        | 6.00 |
$column[width:40%]
**Observed rates**

- Order $k=2$: rate **2.00** ✓
- Order $k=4$: rate **4.00** ✓
- Order $k=6$: rate **6.00** ✓

Matches theoretical prediction $\|e_u\|_{L^2} = \mathcal{O}(h^k)$ for
smooth solutions.
$endcolumns

$note
$content{
Taylor-Couette is the go-to benchmark because the exact solution is known
analytically — no reference solution needed.

Rates of exactly k confirm optimal convergence.  This is expected for smooth
flows but non-trivial to achieve with the pressure stabilisation we use.
}
$endnote

#### $p$-Convergence (Spectral Accuracy)

For a smooth problem, fixing the mesh and increasing $k$ gives **exponential
convergence**:

$$
\|e_u\|_{L^2} \leq C \, e^{-\sigma k}, \qquad \sigma > 0
$$

$box
$caption[color:#2980b9]{Key result}
$content[padding:0.8em]{
At $k=8$ with only 16 elements (128 DOF per direction) we achieve the same
$L^2$ error as a second-order method with 2048 elements (2048 DOF per direction)
— a factor **16× reduction** in total degrees of freedom for equivalent accuracy.
}
$endbox

$note
$content{
This is the central selling point of spectral methods.

The exponential convergence only holds for smooth solutions — in the presence
of shocks or singularities (corners, re-entrant boundaries), the advantage
disappears without additional p-adaptivity.

We address this with AMR in the next section.
}
$endnote

## Scalability

### Parallel Performance

#### Strong Scaling (Lid-Driven Cavity, $Re = 10^4$)

Strong scaling measures wall time versus core count for a fixed problem size
($k=6$, $N_{\rm elem} = 262\,144$, $\approx 200\text{M}$ DOF).

$table
$caption{Strong scaling on Example HPC cluster (AMD EPYC 9654, 384 cores/node)}
$content{
| Cores | Wall time (s) | Speed-up | Efficiency |
|------:|:-------------:|:--------:|:----------:|
| 96    | 1842          | 1.00×    | 100%       |
| 192   | 934           | 1.97×    | 98.5%      |
| 384   | 475           | 3.88×    | 96.9%      |
| 768   | 244           | 7.55×    | 94.3%      |
| 1536  | 127           | 14.5×    | 90.6%      |
| 3072  | 68            | 27.1×    | 84.7%      |
}
$endtable

$note
$content{
Efficiency drops gradually due to increased MPI communication overhead as
the subdomain-to-halo ratio decreases.

84.7% efficiency at 3072 cores (32 nodes) is competitive.  Above this,
communication starts to dominate — we are investigating communication-avoiding
variants of the pressure solver (CA-GMRES).
}
$endnote

# Conclusions

## Summary

### Final Remarks

#### What We Showed

$box
$caption[color:#27ae60]{Summary}
$content[padding:1em]{
1. **Formulation** — inf-sup stable high-order spectral element method for
   incompressible Navier-Stokes with IMEX-RK3 time integration.

2. **Convergence** — optimal $\mathcal{O}(h^k)$ algebraic rates confirmed;
   exponential $p$-convergence for smooth problems.

3. **Efficiency** — spectral accuracy reduces DOF count by up to 16× versus
   second-order methods for equivalent $L^2$ error.

4. **Scalability** — >84% parallel efficiency to 3072 cores on production CFD problems.
}
$endbox

$note
$content{
This slide should land in under 1 minute.  Hit each bullet quickly.

The goal is to leave the audience with 4 clear take-aways before moving to
questions.
}
$endnote

#### Future Work and Open Questions

$columns
$column[width:48%]
**Near-term (6 months)**

- Adjoint-based error estimator for AMR
- GPU port of GLL assembly kernel (CUDA/HIP)
- Benchmark against OpenFOAM on ERCOFTAC cases
$column[width:48%]
**Longer-term**

- Compressible extension (Navier-Stokes-Fourier)
- Uncertainty quantification via stochastic collocation
- Open-source release under LGPL v3
$endcolumns

Thank you — **questions?**

$note
$content{
Expected questions:
Q: Why not use DG?
A: DG has larger stencils and higher communication cost at the same DOF count.
   SEM achieves better efficiency for the same accuracy on smooth meshes.

Q: What preconditioner for the pressure solve?
A: Algebraic multigrid (BoomerAMG via hypre) for the Schur complement.
   This is the current bottleneck at very high core counts.

Q: Plans for turbulence modelling?
A: We are evaluating variational multiscale (VMS) LES — compatible with
   the spectral element framework without extra stabilisation parameters.
}
$endnote
