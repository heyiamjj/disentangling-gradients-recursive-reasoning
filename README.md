# Disentangling Gradient Quality from Architecture in Recursive Reasoning Models

**Paper:** [arXiv:XXXX.XXXXX](https://arxiv.org/abs/XXXX.XXXXX)  
**Authors:** Jatin (JJ), Independent Researcher

---

## TL;DR

Recursive reasoning models HRM (55%) and TRM (87%) show a huge gap on Sudoku. But TRM changed **both architecture and gradient method** simultaneously. We run a controlled experiment isolating just the gradient method and find it explains the entire gap — exact accuracy collapses from 18.9% to 2.2% (8.6×). **Gradient quality, not architecture, is the bottleneck.**

## Results

| Configuration | Token Accuracy | Exact Accuracy |
|---|---|---|
| TRM + 1-step gradient (O(1) memory) | 65.9% | **2.2%** |
| TRM + full BPTT (O(T) memory) | 71.6% | **18.9%** |

Both models use the same flat TRM architecture. The only difference is the gradient method.

## 2×2 Factorial Design

| | Dual L/H (HRM) | Single flat (TRM) |
|---|---|---|
| **1-step gradient (O1)** | 55.0% (HRM paper) | **2.2% (this paper)** |
| **Full BPTT (OT)** | [Future work] | **18.9% (this paper)** |

The community compared HRM diagonally to TRM — confounded architecture with gradient method. We fill the right column to isolate the gradient variable.

## Repository Structure

```
├── paper/                    # LaTeX source + figures
│   ├── paper.tex
│   ├── references.bib
│   └── plots/
├── notebooks/                # Kaggle training notebooks
│   ├── trm_1step_final.ipynb
│   └── trm_fullbp_final.ipynb
├── checkpoints/              # Trained model weights
│   ├── trm_1step_final/      # (epochs ~5000, ~10000)
│   └── trm_fullbp_final/     # (epochs ~5000, ~10000)
├── logs/                     # Full training logs
│   ├── trm_1step.log
│   └── trm_fullbp.txt
├── config/                   # Training configuration
│   ├── trm_1step_run.yaml
│   └── trm_fullbp_run.yaml
├── patches/                  # Exact code changes
│   └── gradient_patch.diff
├── README.md
└── LICENSE
```

## Reproduction

### Quick start
1. Upload `notebooks/trm_1step_final.ipynb` to Kaggle with 2× T4 GPU
2. Run all cells (trains for ~4.5h)
3. The eval cell outputs accuracy numbers at the end

### Details
- **Base code:** [SamsungSAILMontreal/TinyRecursiveModels](https://github.com/SamsungSAILMontreal/TinyRecursiveModels)
- **Dataset:** Sudoku-Extreme from [sapientinc/sudoku-extreme](https://huggingface.co/datasets/sapientinc/sudoku-extreme)
- **Hardware:** 2× NVIDIA Tesla T4 (16GB), PyTorch 2.10, CUDA 12.8
- **Training:** 10,000 epochs, 500+500 examples, float32, AdamW, EMA
- **Gradient patch:** See `patches/gradient_patch.diff` — moves all recursion inside `torch.no_grad()` except the final H-update

### Checkpoints
Pre-trained weights are in `checkpoints/`. To evaluate:
```python
# Load and evaluate (see notebook eval cell for full code)
state = torch.load("checkpoints/trm_1step_final/step_9764")
model.load_state_dict(state)
# Run inference on test data...
```

## Training Curves

![Loss](paper/plots/loss.pdf)
![Exact Accuracy](paper/plots/exact.pdf)

Full BPTT achieves lower loss and higher exact accuracy throughout training. The gap widens over time.

## Citation

```bibtex
@article{jj2026disentangling,
  title={Disentangling Gradient Quality from Architecture in Recursive Reasoning Models},
  author={Jatin (JJ)},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2026}
}
```

## License

MIT — see [LICENSE](LICENSE).

Code based on [SamsungSAILMontreal/TinyRecursiveModels](https://github.com/SamsungSAILMontreal/TinyRecursiveModels) (MIT).
