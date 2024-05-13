from pydantic import (
    AnyHttpUrl,
    AnyUrl,
    BaseModel,
    Field,
    JsonValue,
    TypeAdapter,
    alias_generators,
)
from typing_extensions import (
    Annotated,
    Dict,
    Literal,
    Optional,
    Type,
    TypeAlias,
    TypeVar,
)

#
model_json_properties = dict(
    alias_generator=alias_generators.to_camel,
    populate_by_name=True,
)


# Ensure that union type use `OneOf` in schema
# instead of `anyOf`

# See https://github.com/pydantic/pydantic/issues/656#

T = TypeVar('T')


def one_of(s):
    if 'anyOf' in s:
        s['oneOf'] = s['anyOf']
        del s['anyOf']

# Example: OneOf[str|int] will produce:
# {'oneOf': [{'type': 'string'}, {'type': 'integer'}]} instead of:
# {'anyOf': ... }


OneOf = Annotated[T, Field(json_schema_extra=one_of)]


#
# Fix optional field in json_schema
#
# This will replace schema for Optional[T] as
# { 'type': ..., ... } instead of
# { 'anyof': [{ 'type': ..., ,,,}, { 'type': null }] }
#
def null_field(s):
    schema = s.pop('anyOf')[0]
    s.pop('default', None)
    s.update(schema)


def NullField(**kwargs):
    return Field(default=None, json_schema_extra=null_field, **kwargs)


class JsonModel(BaseModel, **model_json_properties):
    # Override: force by_alias=True
    def model_dump_json(self, *args, **kwargs) -> str:
        return super().model_dump_json(*args, by_alias=True, exclude_none=True, **kwargs)


class Link(JsonModel):
    # Supplies the URI to a remote resource (or resource fragment).
    href: AnyHttpUrl
    # The type or semantics of the relation.
    rel: Optional[str] = NullField()
    # Mime type of the data returne by the link
    mime_type: Optional[str] = NullField(serialization_alias="type")
    # human-readable identifier for the link
    title: str = ""
    # A long description for the link
    description: Optional[str] = NullField()
    # Estimated size (in bytes) of the online resource response
    length: Optional[int] = NullField()
    # Is the link templated with '{?<keyword>}'
    templated: bool = False
    # Language of the resource referenced
    hreflang: Optional[str] = NullField()


#
# Extented link reference for input
# by reference
#
class LinkReference(Link):
    # Http method
    method: Literal["GET", "POST"] = "GET"
    # Request body
    body: Optional[str] = NullField()


def MediaType(
    _type: Type,
    media_type: str,
    *,
    encoding: Optional[str] = None,
    schema: Optional[str] = None,
) -> TypeAlias:

    schema_extra: Dict = {'contentMediaType': media_type}
    if encoding:
        schema_extra.update(contentEncoding=encoding)
    if schema:
        schema_extra.update(contentSchema=schema)

    return Annotated[_type, Field(json_schema_extra=schema_extra)]


class Format(JsonModel):
    media_type: str
    encoding: Optional[str] = None
    schema_: Optional[AnyUrl | Dict[str, JsonValue]] = Field(None, alias="schema")


class QualifiedInputValue(Format):
    value: JsonValue


# Create a typeadapter for Reference/Qualified input
RefOrQualifiedInput = TypeAdapter(QualifiedInputValue | LinkReference)


class InputValueError(Exception):
    pass
