---
notoc: true
---

# Learning Lab: Evaluating a Physics-Constrained Model

**Unit 2 · Lesson 2** — Physically Constrained Surrogate Models

In this lab you are given a pre-trained physics-informed neural network (PINN) that models the thermal behaviour of a liquid-cooled cold plate. Your job is not to build or train the model — it has already been trained against a physics penalty that enforces energy conservation. Your job is to **evaluate** whether it actually behaves physically.

This is the core skill of Unit 2: given a surrogate model that claims to respect physics, can you verify that claim with data?

**Learning objectives:** 8.1-41 Evaluate a trained model's adherence to physical constraints · 8.1-42 Interpret physical-consistency failures in terms of engineering reliability

> **Save your work:** JupyterLite does not auto-save. Use **File → Save** (Ctrl+S) inside the notebook, then **File → Download** before closing the tab.

```{raw} html
<div style="margin-top:1rem;">
  <div id="lab-btn" style="text-align:center;padding:2rem 0 1rem;">
    <button
      onclick="var f=document.getElementById('lab-frame');
               f.setAttribute('src','../lite/notebooks/index.html?path=lab_pinn.ipynb');
               document.getElementById('lab-btn').style.display='none';
               f.style.display='block';"
      style="background:#3776AB;color:#fff;padding:.75rem 2.5rem;border:none;
             border-radius:.4rem;font-size:1.05rem;font-weight:600;cursor:pointer;
             box-shadow:0 2px 6px rgba(0,0,0,.2);">
      &#x1F680; Launch interactive lab notebook
    </button>
    <p style="color:#666;margin:.6rem 0 0;font-size:.85rem;">
      Python runs in your browser via WebAssembly &mdash; no installation needed
    </p>
  </div>
  <iframe id="lab-frame" src="" allow="cross-origin-isolated"
    style="display:none;width:100%;height:calc(100vh - 80px);
           min-height:600px;border:none;">
  </iframe>
</div>
```
