# template-devcontainer-django-pg

This is a starter template to get ready-to-use Django/PostgreSQL project in a local Dev Container.


### Specifications

- Main containers: Python/Django (service_app) and PostgreSQL (service_db)
- Environment variables are handled with `.env` file (via django-environ)
- Linting / Imports auto-sorting: Ruff
- Auto-Formatting: Black
- Package management: Poetry
- No front-end configuration

## How To

#### Before cloning the container:
- Open Docker Desktop and ddd `/workspaces` directory in settings > Resources > File sharing.
- Install [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) in VS Code
- Run `Clone Repository` command and clone this repository.


#### Once the container has been created:
- Reload the container once (running the `reload window` VS Code command ) to ensure there is no error with extension activation due to a Dev Container bug.
- Run `./manage.py migrate`
- Run `./manage.py runserver` and go to "http://localhost:8000/" to ensure everything works.

### About .env file

- .env file is currently versionned because it's required to create the container without error. Once the container is created, you should un-version it by adding it to `.gitignore` file, and running `git rm --cached .env`
# dj-bricks
