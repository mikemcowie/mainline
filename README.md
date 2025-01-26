# Mainline

Get your first line of code into production, in minutes

## The Pitch

We want to keep the developer working with their codebases, discovering and solving problems for their customers.

This'll offer a tool to provide a *golden path* - keep on the rails we provide,and in return, our system will take your code to production - in your cloud or (at least one day) ours.

We'll do it transparently - warts and all of how we build and ship our system will be public.

## Use-cases

### Hobbyists

Hobbyists want cheap hosting that gives them accessn to a few attached services like postgresql, while being *cheap* . While hobbyists won't make a product commercially viable, they are valuably enthusiastic and engaged users , and can also become contributors .

### Freelance/Contract developers

Freelance developers are trying to ship functional code on short time budget, and value having their platform needs taken care of to a high degree of quality.

We help freelance/contract developers get their code deployed, and hence their project as a whole in a great shape to handover as a viable concern when the contract is up.

Mainline could also help these types of efforts get integrated into larger organizations systems, by taking deeper care of those toucher organizational security/governence concerns.

### Who else?

Love to hear if this makes sense to you for another use-case.

## The MVP Goal

The MVP of the system is python-centric - we'll build a system  that can take a python web app, with a limited range of attached services (databases, storage, external APIs) available.

You will be able to declare your infrastructure/[attached services](https://12factor.net/backing-services) deterministically as part of your project definition according to the python [pyproject.toml specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/) supported by modern python tooling.

```toml
[project]
name = "my-system"
requires-python = "==3.13"

### ... everything else you define for your own project

[tool.mainline]
attached-services = [ "postgresql" ]
```

The goal of this system is that if you write a well-formed pyproject.toml [complying generally with the specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/), with that single configuration line for our tool, *is enough for us to build, test and deploy your app for production*/

Of course we'll expose further configuration options to tune the system further, but for everything except that single line, we provide *out of the box, well thought out defaults so that you can focus on shipping code*.

## Isn't this like heroku, openshift, pythonanywhere ... ?

Yeah, I suppose. The key concept is leveraging the standard metadata, and providing a joined-up developer experience to take your code to the cloud in production, with minimal effort on your part.

## What'll it cost?

In pre-MVP stage, I'd support on a *best-effort, don't use in production, hobbiests welcome* basis for hosting costs, feedback, and if you want me to actually be able to spend some time on it, at least some *[koha](https://en.wikipedia.org/wiki/Koha_(custom))* .

I'd consider a limited bare-bones free offering, but I ain't got deep pockets, but it won't hit the marks of production-ready.
