# E255 — AI for Engineering and Scientific Discovery

**Proof-of-concept demo** · WGU MSAIES Program

This site demonstrates two things simultaneously:

1. **How the course learning labs could be hosted** — interactive, in-browser Jupyter notebooks served via JupyterLite with zero server infrastructure.
2. **How the Performance Assessment (PA) task could be hosted** — the same environment, different framing: guided exploration becomes a student-submitted evidence artifact.

Both use the same pre-trained model and dataset. Neither requires students to install Python, PyTorch, or any local dependency — the kernel runs in the browser via Pyodide.

---

## Structure

| Section | What it shows |
|---|---|
| **Learning Lab** | Guided exercise: load a provided physics-constrained model, complete a marked cell, interpret the result. Equivalent to the SSD Unit 2.2 guided lab format. |
| **PA Task 1** | Assessment format: same model and data, student-facing rubric text, evidence computation structured for submission. |

## Technical notes

- **Kernel:** Python (Pyodide) — runs in the browser, no server required.
- **Packages available:** numpy, pandas, matplotlib, scikit-learn, Optuna — the full E255 PA toolchain.
- **Shared assets** (`content/`): `case_physics.py`, `mlp.py`, pre-trained model weights (`pinn.npz`, `surrogate.npz`), and dataset partitions are bundled into the JupyterLite virtual filesystem and importable directly in notebooks.
- **No DeepXDE or PyTorch required** for the PA or these labs — models are provided as pre-trained numpy artifacts.

Click **Learning Lab** or **PA Task 1** in the left sidebar to begin.
