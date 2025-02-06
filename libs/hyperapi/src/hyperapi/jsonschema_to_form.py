from hyperapi.components.form import Form, FormInput
from hyperapi.schemas.json_schema_meta_schema import CoreAndValidationSpecificationsMetaSchema
from pydantic import BaseModel, Field


def to_form_input_type(in_type:str)->str:
    """converts the type of a jsonschema to form input type"""
    match in_type:
        case "string":
            return "string"
        case "integer":
            return "number"
        case _: # Fallback - return the in type and pray for the best
            return in_type
        

def add_properties_to_inputs(form:Form, name:str, property:dict, schema:CoreAndValidationSpecificationsMetaSchema):
        type = property.get("type")
        if type:
            return form.inputs.append(FormInput(type=to_form_input_type(property["type"]), name=name, id=form.id+name, label=property["title"]))
        raise TypeError(f"type must be set. We do not support nested fields")

        

def jsonschema_to_form(form_id:str, action:str, method:str, form_cls: type[Form], schema:dict):
    validated_schema = CoreAndValidationSpecificationsMetaSchema.model_validate(schema)
    form = Form(
        id=form_id,
        action=action,
        method=method,
        inputs=[]
    )
    for key,value in validated_schema.properties.items():
        add_properties_to_inputs(form, key, value, validated_schema)
    return form



class MuleSchema(BaseModel):
    """A model that contains all the types we want to support"""
    basic_string:str
    string_with_field:str = Field(title="A different title")
    basic_int:int



import pytest


@pytest.fixture()
def form():
    return jsonschema_to_form("instance1", "/", "POST", Form, MuleSchema.model_json_schema())

def test_simple_type_annotation_string(form:Form):
    assert form.inputs[0].name == "basic_string"
    assert form.inputs[0].label == "Basic String"
    assert form.inputs[0].type == "string"
    assert form.inputs[0].id == "instance1basic_string"


def test_simple_string_with_field(form:Form):
    assert form.inputs[1].name == "string_with_field"
    assert form.inputs[1].label == "A different title"
    assert form.inputs[1].type == "string"
    assert form.inputs[1].id == "instance1string_with_field"


def test_integer(form:Form):
    assert form.inputs[2].name == "basic_int"
    assert form.inputs[2].label == "Basic Int"
    assert form.inputs[2].type == "number"
    assert form.inputs[2].id == "instance1basic_int"





