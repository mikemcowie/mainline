from enum import StrEnum
from dataclasses import dataclass
from http import HTTPMethod
from dominate import tags as t  # type: ignore
from hyperapi.components.base import Component


class InputType(StrEnum):
    HIDDEN = "hidden"
    EMAIL = "email"
    TEXT = "text"
    NUMBER = "number"


@dataclass
class FormInput:
    type: InputType
    id: str
    name: str
    label: str


@dataclass
class Form(Component):
    id: str
    action: str
    method: HTTPMethod
    inputs: list[FormInput]

    def _build_input(self, input: FormInput):
        with t.div(id=f"{self.id}-input-div-{input.id}"):
            t.input_(
                type=input.type.value, id=f"{self.id}-input-{input.id}", name=input.name
            )
            t.label(input.label, for_=input.name)

    def build(self):
        with t.form(id=self.id, action=self.action, method=self.method.value):
            for input in self.inputs:
                self._build_input(input)

    @classmethod
    def from_json_schema(cls, schema: dict, action: str, method: HTTPMethod):
        inputs: list[list[FormInput]] = []
        for key, value in schema.get("properties", {}).items():
            type = value.get("type")
            inputs.append(
                FormInput(
                    type=value.get("type"),
                    id=f"{key}-{type}",
                    name=key,
                    label=value.get("title"),
                )
            )
        return cls(id=schema.get("title"), action=action, method=method, inputs=inputs)
