# Hackyeah 2025

## Dev workflow

### Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

If you don't have Python3.13 run:

```bash
uv python install 3.13
```

Then create venv:

```bash
uv venv
```

Don't forget to activate it:

```bash
source .venv/bin/activate
```

or on Windows:

```bash
.\.venv\Scripts\activate.bat
```

After that simply run:

```bash
uv sync --dev
```

If you want to add some package run:

```bash
uv add some-package
```

[Some uv cheat sheet can be found here](https://gist.github.com/gwangjinkim/70b353e63492e2bdd37f24b441b128b4).

### Linting & Formatting

```bash
uv run ruff check app/ tests/
```

Consider adding it as a precommit.

We can also add type checking using mypy. The best option is to run [dmypy](https://mypy.readthedocs.io/en/stable/mypy_daemon.html):

```bash
# Start the daemon
uv run dmypy start

# Check files
uv run dmypy check -- app/ tests/

# Stop the daemon when done
uv run dmypy stop
```

### Tests

```bash
uv run pytest tests/ -v
```

### Usage

To run the app in dev mode run command:

```bash
uv run fastapi dev
```

For production code run command:

```bash
uv run fastapi run
```
