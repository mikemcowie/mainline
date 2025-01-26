# Mainline Server

The mainline server is the primary engine of mainline.

## Intended Architecture

Mainline server is intended to be a monolithic application encompassing both browser and programatic use-cases from a
single codebase.

It is built along the lines of [the 12-factor app](https://12factor.net/) as a guiding princple.

### Attached Services


#### Database

mainline-server will be backed by postgresql

#### Other Infra

Other infra may be needed later - caches, queues etc - as/when we find use-cases where postgresql is a poor fit.
However until there is actually an established use-case, it will just use [postgres for everything](https://www.amazingcto.com/postgres-for-everything/).

#### IAM

The IAM approach is not decided, but on the same principle as mainline-server itself is trying to help other developers get a sound foundation, we don't want to reinvent the wheel on IAM, and intend to use a well-established IAM provider.

Under consideration would be one or more of the following

* self-hosted option: [keycloak](https://www.keycloak.org/)
* big-corp option: [google](https://developers.google.com/identity/openid-connect/openid-connect)
* specialist SaaS option: [auth0](https://auth0.com/)
* library option: [fastapi-users](https://fastapi-users.github.io/fastapi-users/)

The last option is *conceptually*  a bridge to support multiple configurable IAM providers as part of the open-source self-hosted server; however do not consider this to be an early priority.


## Get started developing

1. The system is currently developed on Linux; while there's no specific reason it can't work on Windows or Mac, this developer doesn't, so no support is offered at this moment.
2. [Install pre-commit](https://pre-commit.com/#install)
3. [Install the uv package manager](https://docs.astral.sh/uv/).
4. [Ensure docker is installed](https://docs.docker.com/engine/install/) and running.
5. Validate that you can run the test suite with `uv run pytest`. All tests should pass, with 100% coverage reported, if you're checking out from the main branch.
6. Run the server with `uv run mainline-server --dev`. This development entrypoint should support hot reloading, and
   will automatically bring up development instances of all the required attached services via docker.
7. Debug and trace through the system to your hearts content.
