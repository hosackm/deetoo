# deetoo

Database of items in [Diablo 2](https://en.wikipedia.org/wiki/Diablo_II).

## Install and run tests

```bash
uv sync
uv pip install -e .
python deetoo/data/seed.py
fastapi dev deetoo/app.py
curl -sL 'localhost:8000/base_items'
```
