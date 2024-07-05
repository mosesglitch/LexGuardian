LexGuardian
==============================

A chatbot that helps you chat with the Kenyan Law in a simple way.

Project Organization
------------

```
LexGuardian/
├── LICENSE
├── README.md
├── Makefile                     # Makefile with commands like `make data` or `make train`
├── configs                      # Config files (models and training hyperparameters)
│   └── configs.yaml
│
├── data                         # The final, canonical data sets for modeling.
│   └── raw                      # The original, immutable data dump.
│
├── notebooks                    # Jupyter notebooks.
├── app.py                       # The streamlit app
├── pyproject.toml               # The requirements file for reproducing the analysis environment.
└── lex_guardian                          # Source code for use in this project.
    ├── __init__.py              # Makes src a Python module.
    ├── rag.py                   # Containes the RAG code
    ├── utils.py                 # Contains utility code
```
