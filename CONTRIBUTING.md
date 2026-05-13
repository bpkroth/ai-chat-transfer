# Contributing

## Development

### Setup

```bash
uv sync
# Or using make (also installs pre-commit hooks)
make deps
```

### Pre-commit Hooks

Git hooks are automatically installed via `make deps`. To install them manually:

```bash
uv run pre-commit install
```

### Running Tests

```bash
uv run pytest
# Or using make
make test
```

### Linting, Formatting & Type Checking

```bash
# Individual commands
uv run ruff check .
uv run ruff format .
uv run ty check src
uv run pylint src/chat_bridge

# Run all checks via make
make check
```

### All-in-one

```bash
make all
```

## Publishing Releases

Releases are published to PyPI by `.github/workflows/release.yml` when a GitHub
Release is published. The release tag must match the project version in
`pyproject.toml` as `v<version>`, for example `v0.1.0`.

### One-time setup

Create a PyPI API token:

1. Sign in to <https://pypi.org/>.
1. Open **Account settings** -> **API tokens**.
1. Create a token named for this repository.
1. For the first upload of a new project, use an account-scoped token. After the
   project exists on PyPI, replace it with a project-scoped token for
   `chat-bridge`.

Add the token to GitHub as a repository secret named `PYPI_API_TOKEN`.

Using `gh`:

```bash
gh secret set PYPI_API_TOKEN --body "pypi-..."
```

Using the GitHub web interface:

1. Open the repository on GitHub.
1. Go to **Settings** -> **Secrets and variables** -> **Actions**.
1. Click **New repository secret**.
1. Set **Name** to `PYPI_API_TOKEN`.
1. Paste the PyPI token into **Secret** and save it.

### Release with `gh`

1. Update `project.version` in `pyproject.toml`.
1. Commit the version change and push it.
1. Tag the release commit and push the tag:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Create the GitHub Release:

```bash
gh release create v0.1.0 --title "v0.1.0" --generate-notes
```

Watch the publish workflow:

```bash
run_id="$(gh run list --workflow release.yml --limit 1 --json databaseId --jq '.[0].databaseId')"
gh run watch "$run_id"
```

### Release with the web interface

1. Update `project.version` in `pyproject.toml`, commit it, and push it.
1. Open the repository on GitHub.
1. Go to **Releases** -> **Draft a new release**.
1. Create or choose a tag named `v<version>`, such as `v0.1.0`, pointing at the
   release commit.
1. Fill in the title and release notes.
1. Click **Publish release**.

The release workflow runs `make check`, verifies that pre-commit did not change
files, runs tests, builds the package, checks the distributions with Twine, and
uploads the result to PyPI.
