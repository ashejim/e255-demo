# E255 Demo — Jupyter Book on GitHub Pages

Proof-of-concept: E255 learning lab + PA Task 1 hosted as a Jupyter Book with
JupyterLite in-browser execution. No server required for students — Python runs
via Pyodide (WebAssembly) directly in the browser.

## First-time GitHub setup (5 steps)

1. **Create a new GitHub repo** (public or private) named `e255-demo`.

2. **Enable GitHub Pages** in the repo settings:
   - Settings → Pages → Source: **GitHub Actions**

3. **Push this folder** to the repo:
   ```
   cd e255-demo
   git init
   git add .
   git commit -m "initial Jupyter Book demo"
   git branch -M main
   git remote add origin https://github.com/ashejim/e255-demo.git
   git push -u origin main
   ```

4. **Update `_config.yml`** — replace `YOUR_USERNAME` in the `repository.url` field.

5. **Watch the Actions tab** — the `Build and Deploy` workflow runs automatically.
   When it completes (2–4 minutes), the site is live at:
   `https://YOUR_USERNAME.github.io/e255-demo/`

## Testing locally (optional)

```bash
pip install -r requirements.txt
jupyter-book build .
# Open _build/html/index.html in a browser
```

Note: JupyterLite launch buttons require the built site to be served over HTTP,
not opened as a local file. Use `python -m http.server 8080` from `_build/html/`
for local testing.

## What this demonstrates

| Question | What the PoC answers |
|---|---|
| Can Jupyter Book + GitHub Pages host the labs? | Yes — static build, Actions deploy |
| Does JupyterLite run the E255 PA toolchain? | Tested by running the notebooks in-browser |
| Can local modules (case_physics, mlp) be imported? | Tested by the setup cell — check console output |
| Does the two-format (lab + task) structure work? | Yes — two chapters, same assets, different framing |

## Key uncertainty

Module import in JupyterLite depends on `jupyterlite_contents` placing
`case_physics.py` and `mlp.py` at the expected path in the virtual filesystem.
The setup cell tries three paths and falls back to inline definitions if all
fail — check the cell output for "course modules loaded from virtual filesystem"
vs "WARNING: using inline fallback". If the fallback triggers, the fix is a
`jupyterlite_config.json` path adjustment, not a package or toolchain issue.

## Asset provenance

All assets in `content/` are derived from the E255 Task 1 reference
implementation (`task1_test_case/`, 2026-08-30). The physics model, dataset
generator, and model weights are the same ones used to validate the PA rubric.
