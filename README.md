This project is a simple fee calculator I made for an assignment.

# Minimum Supported Python Version
I suggest using 3.14, as it uses the latest syntax.

# Getting Started
Prequisites:
- `uv` from [astral.sh](https://github.com/astral-sh/uv). Recommended, but not necessary.

## With `uv`
Just copy paste these commands. Note that this is more accurate than using `requirements.txt`.
I cannot guarantee that the `requirements.txt` will always be updated or formatted properly.

```sh
git clone https://github.com/prxavv/nssj-calc.git
cd nssj-calc

uv sync
uv run nssj-calc
```

## Without `uv`
If you're not on Windows, follow this:
```sh
git clone https://github.com/prxavv/nssj-calc.git
cd nssj-calc

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install --no-deps -e .
nssj-calc
```

If you are on Windows, this:
```sh
git clone https://github.com/prxavv/nssj-calc.git
cd nssj-calc

python -m venv .venv
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
pip install --no-deps -e .
nssj-calc
```

# Developers
Here I'll talk a little bit about the architecture of the application. There isn't much to it.

```mermaid

```


