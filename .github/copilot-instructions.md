---
description: "Standard Python project conventions and tooling using PieMaker"
---

# Python Project Standards

This repository contains a Python project following a **unified standard** for tooling, build automation, and coding conventions. All projects share the same tooling stack and conventions to ensure consistency and maintainability. The key components of the standard include:

- Build automation (PieMaker)
- Project definition and dependency management (Poetry)
- Code formatting (Black)
- Static analysis (Pylint)
- Testing (Pytest)

This document outlines the common conventions that apply across the Python projects.

## Python Version & Dependencies

- **Python Version**: 3.10+
- **Dependency Manager**: Poetry
- **Lock File**: `poetry.lock` (checked in)
- **Dependency Specification**: `pyproject.toml` (Poetry format)

### Adding Dependencies

```bash
poetry add package_name          # Add to runtime deps
poetry add --group dev pkg_name  # Add to dev deps
make deps                        # Install all deps
```

### VirtualEnv

- **Virtual environment**: `.venv/` (Poetry-managed)
- **PATH prefix**: `.venv/bin:` (binaries available as `pylint`, `black`, `pytest`, etc.)

### Project Structure

```text
project/
├── <module>                  # Main package
│   ├── __init__.py
│   ├── logger.py
│   └── ...
├── examples/                 # Example configs and usage
├── tests/                    # Unit tests
├── tests-integration/        # Integration tests
├── docs/                     # Generated documentation
├── stage/                    # Temporary stage files
├── .coveragerc               # Coverage configuration
├── .github/                  # GitHub workflows & Copilot instructions
├── .gitignore                # Git ignore rules
├── .pylintrc                 # Pylint configuration
├── .rtk.json                 # RTK configuration
├── .venv/                    # Virtual environment (Poetry-managed)
├── avatar.jpg                # Project avatar (80x80 pixels)
├── CHANGELOG.md              # Changelog file following Keep a Changelog format
├── LICENSE                   # License file
├── Makefile                  # Build automation (PieMaker)
├── piemaker.yml              # PieMaker configuration
├── poetry.lock               # Locked dependencies
├── pyproject.toml            # Poetry configuration
├── README.md                 # Project README
└── requirements.txt          # Python dependencies generated from Poetry
```

## Build Automation (PieMaker)

This Python project uses **PieMaker** as a standard build automation tool that unifies the build pipeline across all projects.

### Common Commands

```bash
make ci                # Run full CI pipeline
make all               # Alias for ci
make clean             # Remove temporary, staged, cached files using rm
make stage             # Create stage directory using mkdir
make deps              # Install dependencies using Poetry
make deps-upgrade      # Upgrade dependencies to latest versions using poetry-plugin-up
make rmdeps            # Remove dependency files (`.venv`, `poetry.lock`, `requirements.txt`) using rm
make style             # Check/format code using Black
make lint              # Run static analysis using Pylint
make test              # Run unit tests using Pytest
make test-examples     # Run example shell scripts using bash
make coverage          # Generate coverage reports using coverage.py and unittest
make complexity        # Run complexity analysis using Radon
make doc               # Generate documentation using Sphinx (sphinx-apidoc + make html)
make package           # Build package using Poetry
make install           # Install package into virtual environment using Poetry
make uninstall         # Uninstall package using pip
make reinstall         # Reinstall package using pip + Poetry (`uninstall` then `install`)
make test-integration  # Run integration tests using Pytest
```

### Release Targets

```bash
make release-major     # Create major release using RTK
make release-minor     # Create minor release using RTK
make release-patch     # Create patch release using RTK
```

### Update Targets

```bash
make update-to-latest  # Update Makefile to latest PieMaker tag using curl + GitHub API + jq
make update-to-main    # Update Makefile to PieMaker main branch using curl
make update-to-version # Update Makefile to specific PieMaker version using curl
make update-dotfiles   # Refresh project dotfiles using generator-python (git clone + plop + cp)
```

## Development Environment

This project is designed to be developed in a consistent environment via Docker image `cliffano/studio`.

You can run the container using: `docker run --rm --workdir /opt/workspace -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/opt/workspace -i -t cliffano/studio` and then run the build commands inside the container.

Alternatively you can run the PieMaker Makefile targets via Docker container entrypoint, e.g. `docker run --rm --workdir /opt/workspace -v /var/run/docker.sock:/var/run/docker.sock -v $PWD:/opt/workspace -i -t cliffano/studio make ci`.

## Code Style, Testing, and Detailed Guidance

This file keeps the high-level project defaults. Detailed implementation rules live in scoped instruction files so they are only loaded when relevant.

### Code Style and Linting

- Formatting uses Black via `make style`
- Static analysis uses Pylint via `make lint`
- Detailed Python coding rules are in `.github/instructions/python-code.instructions.md`

### Testing

- Unit tests live in `tests/`
- Integration tests live in `tests-integration/`
- Run tests with `make test` and `make test-integration`
- Detailed testing rules are in `.github/instructions/testing.instructions.md`

### Documentation

- Documentation is generated with Sphinx via `make doc`
- Generated outputs live under `docs/`

Common generated subdirectories under `docs/`:

- `doc/` for generated API documentation
- `coverage/` for coverage reports
- `complexity/` for complexity analysis reports
- `lint/` for lint reports
- `test/` for unit test reports
- `test-integration/` for integration test reports

## Continuous Integration Pipeline

The Makefile (PieMaker) orchestrates standard build targets, with `make ci` running the following steps in sequence:

- clean              # 1. Clean temp files
- deps               # 2. Install dependencies
- style              # 3. Format & check code (black)
- lint               # 4. Static analysis (pylint)
- test               # 5. Unit tests (pytest)
- coverage           # 6. Coverage reports
- complexity         # 7. Complexity analysis
- doc                # 8. Generate documentation
- package            # 9. Build distribution
- reinstall          # 10. Clean install from package
- test-integration   # 11. Integration tests

All steps must pass before code is merged. Developers should run `make ci` locally before pushing to ensure the CI pipeline will pass.

After the code is merged, the CI pipeline will run as Github CI workflow.

## GitHub Workflows

This repository defines the following workflows under `.github/workflows/`:

- **CI** (`ci-workflow.yaml`): Trigger: `push`, `pull_request`, and manual `workflow_dispatch`. Purpose: Runs the full quality pipeline (`make ci`) across a Python version matrix (usually LTS versions), runs example tests, and publishes generated docs to GitHub Pages.

- **CodeQL** (`codeql-analysis.yml`): Trigger: `push` to `main`, `pull_request` targeting `main`, and weekly scheduled run (`cron`). Purpose: Performs GitHub CodeQL static security analysis for Python and uploads code scanning results.

- **Publish** (`publish-workflow.yaml`): Trigger: `push` of any Git tag. Purpose: Builds and installs the package, then publishes it using `make publish` with `PYPI_TOKEN` secret.

- **Release Major** (`release-major-workflow.yaml`): Trigger: Manual `workflow_dispatch`. Purpose: Creates a major release via `cliffano/release-action` (`release_type: major`).

- **Release Minor** (`release-minor-workflow.yaml`): Trigger: Manual `workflow_dispatch`. Purpose: Creates a minor release via `cliffano/release-action` (`release_type: minor`).

- **Release Patch** (`release-patch-workflow.yaml`): Trigger: Manual `workflow_dispatch`. Purpose: Creates a patch release via `cliffano/release-action` (`release_type: patch`).

- **Upgrade Deps** (`upgrade-deps-workflow.yaml`): Trigger: Manual `workflow_dispatch`. Purpose: Upgrades dependencies, runs the main validation/build targets, commits dependency updates, and pushes changes back to the current branch.
