# Learning Lab: Evaluating a Physics-Constrained Model

**Unit 2 · Lesson 2** — Physically Constrained Surrogate Models

In this lab you are given a pre-trained physics-informed neural network (PINN) that models the thermal behaviour of a liquid-cooled cold plate. Your job is not to build or train the model — it has already been trained against a physics penalty that enforces energy conservation. Your job is to **evaluate** whether it actually behaves physically.

This is the core skill of Unit 2: given a surrogate model that claims to respect physics, can you verify that claim with data?

## Learning objectives addressed

- 8.1-41 Evaluate a trained model's adherence to domain-specific physical constraints
- 8.1-42 Interpret physical-consistency failures in terms of engineering reliability

## What you will do

1. Load the provided pre-trained PINN (no training required)
2. Complete a marked cell to compute the energy-balance residual
3. Visualise the residual distribution across the dataset
4. Write a two-sentence engineering interpretation

Open the **Lab Notebook** in the left sidebar to begin.
