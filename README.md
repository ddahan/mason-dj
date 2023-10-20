# 🧱 Django Mason Starter

A fully-featured and __opinionated__ Back-End Django Starter Template for __medium-sized SaaS__ _(work in Progress)_.

## Why?

When starting a project from scratch, there is a lot of boilerplate to write to setup tech aspects. The purpose is to split the technical aspects to be able to work almost only in business logic then. 
It also acts as a collection of personal knowledge that can be reused.


## Features

### 🤓 Top-notch Developer Experience with tight VS Code integration

- [x] [VS Code devcontainers](https://code.visualstudio.com/docs/devcontainers/containers) to share the same local environment between all team members with 1-click install
- [x] docker-compose for multiple services (Django, Postgres, Redis, etc.)
- [x] Debug: ipdb + VS Code debug + [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar/)
- [x] VS Code tests, and tasks configured
- [x] Multi linting + auto-formatting + import sorting using [Ruff](https://github.com/charliermarsh/ruff) and its VS Code [extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [x] [ipython](https://ipython.org/) and [django-extensions](https://github.com/django-extensions/django-extensions) for using Python in CLI
- [x] Pre-commit githook to ensure code quality
- [x] Poetry setup using a single `pyproject.toml` file for all config


### 🫙 Database
- [x] [PostgreSQL](https://www.postgresql.org/) + [dj-database-url](https://github.com/jazzband/dj-database-url)
- [x] Local tools (custom data loading/dumping)
- [x] Custom database UML generation command using [D2](https://d2lang.com/)


### ✅ Django best practices

- [x] [12 Factors](https://12factor.net/) compliance with [django-environ](https://github.com/joke2k/django-environ)
- [x] [Compositional Model Behaviors](https://blog.kevinastone.com/django-model-behaviors) for DRY, readable, reusable, testable models and querysets. 
- [x] Security in mind (settings, cors headers, custom admin url, etc.)
- [x] Clean folders structure, with scaling in mind
- [x] Applicative Parameters (in-db parameters to configure app without pushing code)
- [x] Custom User, custom Exceptions

### 🦄 CRUD App
- [x] REST API using [django-ninja](https://github.com/vitalik/django-ninja), with built-in OpenAPI documentation. Uses token-based authentication.
- [x] Unit tests with [pytest](https://github.com/pytest-dev/pytest-django/) and [factory boy](https://github.com/FactoryBoy/factory_boy/)
- [x] Admin


### 🔨 Custom utils
- [x] various utility functions
- [x] custom mixins/fields for Compositional Model Behaviours
- [x] custom decorators


### 🦄 Other features
- [x] Full [Celery](https://docs.celeryq.dev/en/stable/) setup, including [django-celery-beat](https://github.com/celery/django-celery-beat) and [django-celery-results](https://github.com/celery/django-celery-results)
- [x] Soketi server (Open-source Pusher-like for realtime bi-directional messages)
- [x] Mailing integration with SMTP
- [x] More models & fields (PriceField, PositionField, PhoneNumberField, etc.)


## Todo
- [ ] [Django safe delete](https://github.com/makinacorpus/django-safedelete) to soft delete objects
- [ ] [Django Hijack](https://github.com/django-hijack/django-hijack) to work on behalf of others
- [ ] Python 3.11 -> Python 3.12
- [ ] Full Stack Monitoring with Highlight.io (Errors, logs, performance monitoring)
- [ ] User groups and permissions examples
- [ ] Test coverage tool
- [ ] Cache mechanisms
- [ ] Feature flags
- [ ] Social-auth integration  
- [ ] Type hints with [django-stubs](https://github.com/typeddjango/django-stubs) and strict mode on.
- [ ] docker-compose production example (differs from the local one)
- [ ] S3 storage management with [boto3](https://github.com/boto/boto3) and [django-storages](https://github.com/jschneier/django-storages/)
- [ ] [Django-fsm](https://github.com/viewflow/django-fsm) (finite state machines)
- [ ] GraphQL integration with [Strawberry](https://github.com/strawberry-graphql/strawberry-graphql-django)
- [ ] Mail templates using [Maizzle](https://maizzle.com/)
- [ ] DX: `shell_plus` autoreload
- [ ] More advanced API features (pagination, other auth, etc.)
- [ ] Integrations with other SaaS (_it could take some time 😅_) :
  - [ ] Payment → [Stripe](https://stripe.com)
  - [ ] Customer Service → [Freshdesk](https://www.freshworks.com/freshdesk/) or [Intercom](https://www.intercom.com/)
  - [ ] Basic Analytics → [Plausible](https://plausible.io/)
  - [ ] Advanced Product Analytics → [Mixpanel](https://mixpanel.com/)
  - [ ] SMS/Phone → [Twilio](https://www.twilio.com/)
  - [ ] CRM: [Hubspot](https://www.hubspot.com/)
  - [ ] Intelligent Search → [Algolia](https://www.algolia.com/)
  - [ ] Enterprise chat → [Slack](https://slack.com/)
  - [ ] Team Projects → [Notion](https://www.notion.so/)
  - [ ] Business Inteligence → [Metabase](https://www.metabase.com/)
- [ ] Add a documentation to this template using a tool like [Gitbook](https://www.gitbook.com/)

## Related project
- [ ] 🧱 **Nuxt Mason Starter**: the front-end counterpart of this template, using [Nuxt.js](https://nuxt.com/) (vue.js), and [Nuxt UI](https://ui.nuxt.com/).


## FAQ

> Why not using the front-end part of Django?

For a significant part of medium-sized projects, Django front-end abilities are unfortunately not enough to ensure a great UX/DX, compared to tools like React or Vue. [Htmx](https://htmx.org/) kind of fills the gap, but it currently lacks a proper integration with Django and a good developer experience. Besides, a Nuxt Mason Starter (cf. above) should be developped to have the front-end counterpart of this template.

> What if I (or other team members) are not using VS Code?

The whole DX part of this template is focused on VS Code so you would lose these specific features. Besides, if there are different code editors within your team, you should add configuration tools that work between multiple IDEs, like [EditorConfig](https://editorconfig.org/).

> How do you pick the tools of this template?

- I try to pick tools that are suitable for **small to medium start-ups**. You never should start too big. I try to avoid complex concepts that can be more harmful than useful (kubernetes, micro-services)

- I try to favor **multi-usages tools** to have less tools in the end. For example, PostgreSQL can be used for sql **and** nosql, Redis can be used as a message broker **and** a cache mechanism, etc.

- I try to favor **open-source tools** which allow the user to self-host tool or using a paying SaaS (like highlight.io)

- When adding integrations, I try to pick the ones that are **broadly used** rather than the "best" ones.

- I try to **avoid in-progress work** that should change (That's the reason I prefer using Soeti to django-channels or anything async with Django).
