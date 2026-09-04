---
notoc: true
---

# PA Task 1: Physically Constrained Modeling and Surrogate Evaluation

**Assessment code:** XZN1 · Task 1 &nbsp;·&nbsp; **Competency:** 8.1 — Develops and Evaluates Physically Constrained AI Models

This task requires you to evaluate a provided physics-informed surrogate model of a liquid-cooled cold-plate thermal system. You are not asked to build the model from scratch. You will load the provided pre-trained model, run the required validation checks, and write engineering interpretations of the results.

**Submit:** your executed notebook (all cells run, all outputs saved) · written responses in sections marked *Student:* · completed Surrogate Performance Log

> **Save your work:** JupyterLite does not auto-save. Use **File → Save** (Ctrl+S) inside the notebook, then **File → Download** before closing the tab.

```{raw} html
<div style="margin-top:1rem;">
  <div id="task1-btn" style="text-align:center;padding:2rem 0 1rem;">
    <button
      onclick="var f=document.getElementById('task1-frame');
               f.setAttribute('src','../lite/notebooks/index.html?path=task1_pa.ipynb');
               document.getElementById('task1-btn').style.display='none';
               f.style.display='block';"
      style="background:#2d6a4f;color:#fff;padding:.75rem 2.5rem;border:none;
             border-radius:.4rem;font-size:1.05rem;font-weight:600;cursor:pointer;
             box-shadow:0 2px 6px rgba(0,0,0,.2);">
      &#x1F680; Launch Task 1 notebook
    </button>
    <p style="color:#666;margin:.6rem 0 0;font-size:.85rem;">
      Python runs in your browser via WebAssembly &mdash; no installation needed
    </p>
  </div>
  <iframe id="task1-frame" src="" allow="cross-origin-isolated"
    style="display:none;width:100%;height:calc(100vh - 80px);
           min-height:600px;border:none;">
  </iframe>
</div>
```

---

> **Note for evaluators:** Sections A–K correspond directly to Requirements A–K in the task directions. Each section opens with the Competent-level rubric descriptor so the evidence requirement is visible alongside the evidence.
