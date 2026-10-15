# Contributing to zoo-wes-runner

Thank you for your interest in contributing to `zoo-wes-runner`! This document provides guidelines for contributing to the project.

## Overview

`zoo-wes-runner` is a Python library that acts as a plugin for the [ZOO-Project](https://github.com/ZOO-Project/ZOO-Project), enabling it to submit jobs to a [Workflow Execution Service (WES)](https://ga4gh.github.io/workflow-execution-service-schemas/docs/). This allows the ZOO-Project to run an Application Package encoded in CWL across a number of different execution environments. The project uses [Hatch](https://hatch.pypa.io/) as its build and development tool.

---

> **Important:** Always open your Pull Request against the `develop` branch, **not** `main`.
> Pull Requests targeting `main` directly will not be accepted.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- [Hatch](https://hatch.pypa.io/latest/install/) (`pip install hatch`)
- Access to a Workflow Execution Service (e.g. a [TOIL](https://toil.readthedocs.io) WES server) for integration testing

### Development Setup

1. **Fork and Clone**

   ```bash
   git clone https://github.com/ZOO-Project/zoo-wes-runner.git
   cd zoo-wes-runner
   ```

2. **Install Hatch**

   ```bash
   pip install hatch
   ```

3. **Enter the Default Development Environment**

   Hatch automatically creates and manages a virtual environment for you:

   ```bash
   hatch shell
   ```

   This installs all dependencies defined under `[tool.hatch.envs.default]` in `pyproject.toml`.

4. **Verify Installation**

   ```bash
   python -c "from zoo_wes_runner import ZooWESRunner; print('OK')"
   ```

---

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Use these prefixes:

- `feature/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation updates
- `refactor/` — Code refactoring
- `test/` — Test additions or fixes

### 2. Make Changes

Follow the coding standards described in the [Code Standards](#code-standards) section below.

### 3. Run Tests

The project uses `nose2` for testing via a dedicated Hatch environment:

```bash
# Run tests
hatch run test:test

# Run tests with verbose output
hatch run test:testv

# Run tests with coverage report
hatch run test:cov
```

Tests run across Python 3.10, 3.11, and 3.12 as defined in the matrix in `pyproject.toml`.

### 4. Update Documentation

- Update docstrings in the source code
- Update relevant `.md` files in `docs/`
- If adding new configuration options (e.g. WES endpoint, TOIL/SLURM setup), update the configuration documentation
- If changing the installation or server configuration steps, update the installation documentation

To serve the docs locally:

```bash
hatch run docs:serve
```

### 5. Commit Changes

Write clear, conventional commit messages:

```bash
git add .
git commit -m "feat: add support for custom WES authentication headers"
```

Commit types:

- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation only
- `style` — Formatting, no logic change
- `refactor` — Code restructuring
- `test` — Adding or updating tests
- `chore` — Maintenance, dependency updates

### 6. Push and Create a Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:

- **Base branch set to `develop`** - this is required
- A clear title and description
- Reference to any related issues (`Closes #123`)
- A summary of what changed and why
- Notes on any breaking changes

> **Reminder:** The base branch of your PR must be `develop`, not `main`.
> `main` is only updated by maintainers when cutting a release from `develop`.

---

## Hatch Environments

The project defines three Hatch environments in `pyproject.toml`:

| Environment | Purpose | Key Command |
|---|---|---|
| `default` | Day-to-day development | `hatch shell` |
| `test` | Running tests and coverage | `hatch run test:test` |
| `docs` | Building and serving docs | `hatch run docs:serve` |

> **Note:** The `default` and `test` environments use `PIP_EXTRA_INDEX_URL=https://test.pypi.org/simple/` to resolve ZOO-Project packages. Make sure this is accessible in your environment.

---

## Code Standards

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use **type hints** on all public methods
- Use **Google-style docstrings**
- Format code with `black` (line length 100) and sort imports with `isort` (`black` profile), as configured in `pyproject.toml`
- Minimum Python version: **3.10** (for testing); the package itself supports **3.8+**

**Good example:**

```python
def get_wes_run_id(self, cwl_workflow: str) -> str:
    """
    Submit a CWL workflow to the configured WES endpoint.

    Args:
        cwl_workflow: Path or URL to the CWL workflow document.

    Returns:
        The run ID returned by the WES server.

    Raises:
        ValueError: If cwl_workflow is empty or invalid.
    """
    if not cwl_workflow:
        raise ValueError("cwl_workflow must not be empty")
    ...
```

### Error Handling

Catch specific exceptions and use structured logging via `loguru`:

```python
from loguru import logger

def load_config(self, path: str) -> dict:
    """Load configuration from a YAML file."""
    try:
        with open(path) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.warning(f"Config file not found: {path}")
        return {}
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in {path}: {e}")
        raise
```

### Versioning

The package version is managed in `zoo_wes_runner/__about__.py`. Do **not** manually edit the version; it is updated as part of the release process.

---

## Testing Guidelines

### Unit Tests

Place unit tests under `tests/` and name files `test_*.py`:

```python
# tests/test_runner.py
import unittest
from zoo_wes_runner import ZooWESRunner

class TestZooWESRunner(unittest.TestCase):

    def test_initialization(self):
        """Test that the runner initializes correctly."""
        conf = {"lenv": {"message": ""}}
        runner = ZooWESRunner(conf)
        self.assertIsNotNone(runner)
```

### Coverage

Aim for **>80%** code coverage. Run the coverage report with:

```bash
hatch run test:cov
```

Coverage configuration is defined in `pyproject.toml` under `[tool.coverage.*]`.

---

## Documentation

Docs are written in Markdown under `docs/` and built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). The documentation is split into configuring the TOIL server on a SLURM headnode, configuring EOEPCA to use the TOIL server, and submitting jobs and debugging.

When contributing a new feature, update the relevant doc file or add a new one and register it in `mkdocs.yml`.

To preview docs locally:

```bash
hatch run docs:serve
```

To deploy docs (maintainers only):

```bash
hatch run docs:deploy
```

---

## Release Process

Releases are managed by project maintainers:

1. Ensure all changes are merged into `develop` and tested
2. Update the version in `zoo_wes_runner/__about__.py`
3. Update `CHANGELOG.md` (if present)
4. Merge `develop` into `main`
5. Create and push a release tag
6. Build and publish the package:

   ```bash
   hatch build
   hatch publish
   ```

---

## Getting Help

- **Bug reports / feature requests**: [Open an issue](https://github.com/ZOO-Project/zoo-wes-runner/issues)
- **Contact**: Email the maintainers

---

## Code of Conduct

We are committed to a welcoming and inclusive environment. When participating:

- Be respectful of differing viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the project and community
- Show empathy towards other contributors

---

## License

By contributing, you agree that your contributions will be licensed under the **Apache License 2.0**, the same license as this project.

---

Thank you for contributing! 🎉