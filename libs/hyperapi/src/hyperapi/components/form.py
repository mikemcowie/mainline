from dataclasses import dataclass
from http import HTTPMethod

import structlog
from dominate import tags as t  # type: ignore

from hyperapi.components.base import Component

logger = structlog.get_logger()


@dataclass
class FormInput:
    type: str
    id: str
    name: str
    label: str
    required: bool
    example: str | None


@dataclass
class Form(Component):
    id: str
    title: str
    action: str
    method: HTTPMethod
    inputs: list[FormInput]

    def _build_input(self, input: FormInput):
        with t.div(id=f"{self.id}-input-div-{input.id}"):
            t.label(input.label, for_=input.name, cls="form-label")
            input_attrs = dict(
                cls="form-control",
                type=input.type,
                id=f"{self.id}-input-{input.id}",
                name=input.name,
            )
            if input.required:
                input_attrs["required"] = 1
            if input.example:
                input_attrs["placeholder"] = input.example

            t.input_(input_attrs)

    def build(self):
        with t.form(
            {
                "id": self.id,
                "action": self.action,
                "method": self.method,
                f"hx-{self.method.lower()}": self.action,
                "hx-trigger": "click",
                "hx-target": "main",
                "hx-swap": "outerHTML",
                "hx-push-url": "true",
            }
        ) as form:
            t.h3(self.title)
            for input in self.inputs:
                with t.div(cls="mb3"):
                    self._build_input(input)
            t.br()
            t.button(
                "Submit",
                {
                    "cls": "btn btn-primary",
                },
            )
            return form

    @classmethod
    def from_json_schema(
        cls, title: str, schema: dict, action: str, method: HTTPMethod
    ):
        inputs: list[list[FormInput]] = []
        properties = schema.get("properties", {})
        for key, value in properties.items():
            examples = properties.get(key).get("examples")
            inputs.append(
                FormInput(
                    type=value.get("type"),
                    id=f"{key}-{value.get('type')}",
                    name=key,
                    label=value.get("title"),
                    required=key in schema.get("required", []),
                    example=examples[0] if examples else None,
                )
            )
        return cls(
            title=title,
            id=schema.get("title"),
            action=action,
            method=method,
            inputs=inputs,
        )
