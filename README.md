# Cookiecutter PyProject 2025

[Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for a Python project.

*   GitHub repo: [https://github.com/AlonKellner/cookiecutter-pyproject-2025/](https://github.com/AlonKellner/cookiecutter-pyproject-2025/)
*   Free software: MIT license

## Features

*   Testing setup with pytest
*   GitHub Actions testing: Setup to easily test for Python 3.13
*   Command line interface using [Typer](https://typer.tiangolo.com/)
*   [astral.sh](https://github.com/astral-sh) stack ([uv](https://docs.astral.sh/uv/), [ruff](https://docs.astral.sh/ruff/), [ty](https://docs.astral.sh/ty/))

## **2025 EXTRA FEATURES**
*   Modern tooling ([tox](https://tox.wiki/en/4.28.4/), [typos](https://github.com/crate-ci/typos), [ties](https://alonkellner.com/ties/), [commitlint](https://commitlint.js.org/), [mkdocs-material](https://squidfunk.github.io/mkdocs-material/))
*   Security ([devcontainers](https://code.visualstudio.com/docs/devcontainers/containers), [pysentry](https://github.com/pysentry-rs/pysentry), [osv-scanner](https://google.github.io/osv-scanner/))
*   Formatters & Linters for all file types ([biomejs](https://biomejs.dev/), [yamlfmt](https://github.com/google/yamlfmt) [taplo](https://taplo.tamasfe.dev/), [rumdl](https://docs.rs/rumdl/latest/rumdl/), [lychee](https://lychee.cli.rs/))
*   AI Agent Supercharged ([Cursor](https://docs.cursor.com/en/welcome), [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview), [MCP](http://modelcontextprotocol.io/docs/getting-started/intro), [lintok](https://github.com/AlonKellner/lintok))

## Quickstart

### Prerequisites
-   [uv](https://docs.astral.sh/uv/getting-started/installation/)
-   [gh](https://docs.github.com/en/github-cli)
-   [Generate a GPG key and add it to github](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key)
-   [Configure a GPG key as your signing key](https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key)

### Steps
*   Generate a Python project:

    ```bash
    uvx cookiecutter https://github.com/AlonKellner/cookiecutter-pyproject-2025.git
    ```

*   Create a GitHub repo:

    ```bash
    cd ./your-new-repo
    gh auth login
    gh repo create "Your Repo Name" --source=. --public
    ```

*   Add a [github access token](https://github.com/settings/personal-access-tokens) to ./.devcontainer/.env:

    ```bash
    echo "GITHUB_PERSONAL_ACCESS_TOKEN=<token-here>" > ./.devcontainer/.env
    ```

*   Open using VSCode (or Cursor):
    *   `ctrl+shift+p`/`cmd+shift+p`
    *   Type "Reopen"
    *   Select `Reopen in Container`
    *   Wait until everything finished loading/running

*   Init commit:

    ```bash
    git add .
    git commit -m "init: cookiecutter"
    git push
    ```

*   Start using your new repo!

### Optional Steps

*   To activate the docs using github-pages:
    *   Go to your repository on GitHub
    *   `Settings -> Pages -> Build and deployment -> Branch`
    *   Select `gh-pages`
    *   Open your docs under `https://<your-username>.github.com/<your-repo-name>`
*   To enable the github actions CI workflow:
    *   Create a `DOCKERHUB_TOKEN`:
        *   Login to [DockerHub](https://app.docker.com/)
        *   `Settings -> Personal access tokens -> Generate new token`
        *   Make sure to set the `Access permissions` to `Read & Write`
        *   Copy and keep your new `DOCKERHUB_TOKEN` for the next steps
    *   Configure your DockerHub user on GitHub:
        *   Go to your repository on GitHub
        *   `Settings -> Secrets and Variables -> Actions -> Branch`
        *   Create a new variable called `DOCKERHUB_USERNAME` for pushing CI images
        *   Create a new secret called `DOCKERHUB_TOKEN` for pushing CI images

## Not Exactly What You Want?

Don't worry, you have options:

### Fork This / Create Your Own

If you have differences in your preferred setup, I encourage you to fork this
to create your own version. Or create your own; it doesn't strictly have to
be a fork.

### Similar Cookiecutter Templates

Explore other forks to get ideas. See the [network](https://github.com/AlonKellner/cookiecutter-pyproject-2025/network) and [family tree](https://github.com/AlonKellner/cookiecutter-pyproject-2025/network/members) for this repo.

### Or Submit a Pull Request

I also accept pull requests on this, if they're small, atomic, and if they
make my own packaging experience better.
