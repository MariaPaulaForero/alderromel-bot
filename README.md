To activate venv:

```bash
python -m venv .venv
source .venv/bin/activate
```

To install dependencies:

```bash
python -m pip install .
pip install "uvicorn[standard]"
pip install opencv-python
```

Para ejecutar el servidor (Si, en español pa que se arrechen):

```bash
PYTHONPATH=./src uvicorn server.main:app --reload --port 8050
```
