
# Phishing URL Detector: PyTorch + Local LLM Triage

A phishing URL classifier trained on Apple Silicon (PyTorch MPS), with a local LLM (Ollama) that writes SOC-style triage notes for flagged URLs. Everything runs offline on a Mac mini.

## Pipeline
1. **Baseline:** logistic regression on 8 hand-crafted URL features (length, dots, hyphens, digits, `@`, IP address, HTTPS).
2. **Neural network:** character-level CNN in PyTorch that learns its own patterns from raw text. Trains in seconds on the Mac GPU.
3. **LLM triage:** URLs scoring 50% or higher are sent to a local Llama 3.2 model, which returns a verdict, reasons and a recommended action.

## Key finding: the 99.5% score was a shortcut
| Model | Recall (phishing) | Real legit URLs flagged |
|---|---|---|
| Full-URL CNN | 99.5% | 5 of 5 |
| Domain-only CNN | 72% (precision 93%, accuracy 87%) | 1 of 6 |

The first model looked almost perfect, but it flagged every real legitimate URL tested (python.org, GitHub, BBC, GOV.UK). Investigation showed that the dataset's legitimate URLs are almost all bare `https://www.` homepages, so the model had learned "has a path or no HTTPS = phishing".

**Fix:** train on the domain only, and remove duplicate domains so no domain appears in both training and test data. Accuracy dropped to 87%, but that score is honest, and the model now behaves sensibly on real-world URLs.

## Limitations
- A domain-only model can't catch phishing hosted on legitimate or compromised domains.
- Subdomains of legitimate sites (for example `docs.python.org`) can be over-flagged, because of how this dataset was built.
- The LLM can make factual mistakes, so it explains decisions but never makes them.

## Tech
Python 3.12 · uv · PyTorch (MPS) · scikit-learn · pandas · JupyterLab · Ollama (Llama 3.2 3B)

Dataset: [PhiUSIIL Phishing URL Dataset](https://archive.ics.uci.edu/dataset/967) (UCI ML Repository, 235,795 URLs)

## Run it
