"""Tiny numpy MLP with optional physics-penalty gradient hook.

Pure numpy so the test case runs with no torch install. The course's real
scaffold would use torch; the mechanics (composite loss = data + weighted
physics penalties) are identical.
"""
import numpy as np


class MLP:
    """Fully connected net, tanh hidden layers, linear output."""

    def __init__(self, sizes, seed=0):
        rng = np.random.default_rng(seed)
        self.W = [rng.normal(0.0, np.sqrt(2.0 / (m + n)), (m, n))
                  for m, n in zip(sizes[:-1], sizes[1:])]
        self.b = [np.zeros(n) for n in sizes[1:]]

    def forward(self, X):
        self._acts = [X]
        h = X
        last = len(self.W) - 1
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            z = h @ W + b
            h = np.tanh(z) if i < last else z
            self._acts.append(h)
        return h

    def backward(self, dY):
        """dY = dLoss/dOutput. Returns (dW list, db list)."""
        gW = [None] * len(self.W)
        gb = [None] * len(self.b)
        d = dY
        for i in reversed(range(len(self.W))):
            gW[i] = self._acts[i].T @ d
            gb[i] = d.sum(axis=0)
            if i > 0:
                h = self._acts[i]           # tanh activation of layer i-1
                d = (d @ self.W[i].T) * (1.0 - h * h)
        return gW, gb

    def params(self):
        return self.W + self.b

    def n_params(self):
        return sum(p.size for p in self.params())


def train(model, Xs, Ys, physics_fn=None, epochs=4000, lr=0.01, verbose_every=1000):
    """Full-batch Adam. Xs/Ys standardized.

    physics_fn(Yhat_std) -> (physics_loss, dLoss/dYhat_std), or None for a
    plain (unconstrained) surrogate. Returns per-epoch loss history.
    """
    params = model.params()
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    b1, b2, eps = 0.9, 0.999, 1e-8
    n = len(Xs)
    history = []

    for epoch in range(1, epochs + 1):
        Yhat = model.forward(Xs)
        err = Yhat - Ys
        data_loss = float(np.mean(err ** 2))
        dY = 2.0 * err / (n * Ys.shape[1])

        phys_loss = 0.0
        if physics_fn is not None:
            phys_loss, dY_phys = physics_fn(Yhat)
            dY = dY + dY_phys

        gW, gb = model.backward(dY)
        grads = gW + gb
        for j, (p, g) in enumerate(zip(params, grads)):
            m[j] = b1 * m[j] + (1 - b1) * g
            v[j] = b2 * v[j] + (1 - b2) * g * g
            mhat = m[j] / (1 - b1 ** epoch)
            vhat = v[j] / (1 - b2 ** epoch)
            p -= lr * mhat / (np.sqrt(vhat) + eps)

        history.append((data_loss, float(phys_loss)))
        if verbose_every and epoch % verbose_every == 0:
            print(f"  epoch {epoch:5d}  data {data_loss:.5f}  physics {phys_loss:.5f}")
    return history


def save(model, path, **extras):
    arrays = {f"W{i}": W for i, W in enumerate(model.W)}
    arrays.update({f"b{i}": b for i, b in enumerate(model.b)})
    arrays.update(extras)
    np.savez(path, **arrays)


def load(path):
    z = np.load(path)
    n_layers = sum(1 for k in z.files if k.startswith("W"))
    sizes = [z["W0"].shape[0]] + [z[f"W{i}"].shape[1] for i in range(n_layers)]
    model = MLP(sizes)
    model.W = [z[f"W{i}"] for i in range(n_layers)]
    model.b = [z[f"b{i}"] for i in range(n_layers)]
    extras = {k: z[k] for k in z.files if not (k[0] in "Wb" and k[1:].isdigit())}
    return model, extras
