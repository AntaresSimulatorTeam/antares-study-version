## Project setup

➢ To install your development environment inside a [virtual environment](https://docs.python.org/3/library/venv.html), run:

```shell
python -m venv venv
source venv/bin/activate
```

➢ To install the project dependencies, then run:
```shell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

or `requirements-dev.txt` if you want to run the tests or check the lint.

## Development tasks

➢ To format and lint the source code with [ruff](https://docs.astral.sh/ruff/), run:

```shell
ruff check src/ tests/ --fix && ruff format src/ tests/
```

➢ To run the tests, run:

```shell
pytest
```

at the root of the projet.

➢ To generate the test coverage report, run:

```shell
 pytest --cov --cov-report xml
```
at the root of the project.

This command will run the unit tests and generate a coverage report inside the `coverage.xml` file at the root of the project.

➢ To check the typing with [mypy](http://mypy-lang.org/), run:

```shell
mypy --install-types --non-interactive
```

## Generating the documentation

➢ First you need to install mkdocs dependencies, so run:

```shell
pip install -r requirements-doc.txt
```

➢ To generate the documentation with [mkdocs](https://www.mkdocs.org/), run:

```shell
mkdocs build -f mkdocs.yml
```

This command will delete the existing documentation folder and regenerate it inside the directory `site`.

➢ To serve the documentation locally, run:

```shell
mkdocs serve -f mkdocs.yml
```

This command will start a local web server to serve the documentation
at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
