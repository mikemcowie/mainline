import sys
from pathlib import Path
import datamodel_code_generator.__main__
import subprocess

JSONSCHEMA_SCHEMA_URL = "https://json-schema.org/draft/2020-12/schema"

schemas_dir = (Path(__file__).parent / "src" / "hyperapi" / "schemas").resolve()

cmd = [
    "datamodel-codegen",
    "--url",
    JSONSCHEMA_SCHEMA_URL,
    "--use-annotated",
    "--use-generic-container-types",
    "--use-non-positive-negative-number-constrained-types",
    "--enum-field-as-literal",
    "one",
    "--use-standard-collections",
    "--use-unique-items-as-set",
    "--capitalise-enum-members",
    "--use-field-description",
    "--target-python-version",
    "3.13",
    "--use-schema-description",
    "--use-double-quotes",
    "--additional-imports",
    "typing.FrozenSet",
    "--output-model-type",
    "pydantic_v2.BaseModel",
    "--output",
    str(schemas_dir / "json_schema_meta_schema.py"),
]
sys.exit(subprocess.run(cmd).returncode)
