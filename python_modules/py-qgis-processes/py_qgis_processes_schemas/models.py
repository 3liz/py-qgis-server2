
import mimetypes

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
    Self,
    Type,
    TypeAlias,
    TypeVar,
    cast,
)

from py_qgis_contrib.core.condition import assert_precondition

#
model_json_properties = dict(
    alias_generator=alias_generators.to_camel,
    populate_by_name=True,
)

JsonDict: TypeAlias = Dict[str, JsonValue]


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


OneOf: TypeAlias = Annotated[T, Field(json_schema_extra=one_of)]


#
# Recursively removo autogenerated title from
# schema properties
#
def remove_auto_title(schema: JsonDict):
    match schema:
        case {'type': 'object', 'properties': dict(props)}:
            for k, v in props.items():
                v = cast(JsonDict, v)
                title = v.get('title')
                if title and cast(str, title).lower().replace(' ', '_') == k.lower():
                    v.pop('title')
                remove_auto_title(cast(JsonDict, v))
        case {'oneOf': seq} | {'allOf': seq} | {'anyOf': seq}:
            for v in cast(list, seq):
                remove_auto_title(cast(JsonDict, v))


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

    @classmethod
    def model_json_schema(cls, *args, **kwargs) -> JsonDict:
        schema = super(cls, cls).model_json_schema(*args, **kwargs)
        remove_auto_title(schema)
        return schema

    # Override: force by_alias=True
    def model_dump_json(self, *args, **kwargs) -> str:
        return super().model_dump_json(*args, by_alias=True, exclude_none=True, **kwargs)


class _LinkBase(JsonModel):
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
#  Generic link
#
class Link(_LinkBase):
    # Supplies the URI to a remote resource (or resource fragment).
    href: str = Field(json_schema_extra={'format': 'uri-reference'})


#
# Define HTTP link
#
class LinkHttp(_LinkBase):
    href: AnyHttpUrl


#
# Extented link reference for input/output
# by reference
#
class LinkReference(LinkHttp):
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
    encoding: Optional[str] = NullField()
    schema_: Optional[AnyUrl | JsonDict] = NullField(alias="schema")


class QualifiedInputValue(Format):
    value: JsonValue

# Create a typeadapter for Reference/Qualified input


RefOrQualifiedInput = TypeAdapter(QualifiedInputValue | LinkReference)

# Prevent name collision with formats.Format
OutputFormat = Format

#
# Mixin class for handling output format in
# input parameters with auto-created output -
# like destination parameters
#

AnyFormat = Format(media_type="application/octet-stream")


class OutputFormatDefinition:
    _output_format: OutputFormat = AnyFormat
    _output_ext: str = ''

    def is_any(self) -> bool:
        return self.output_format.media_type == AnyFormat.media_type

    @property
    def output_format(self) -> OutputFormat:
        return self._output_format

    @output_format.setter
    def output_format(self, value: OutputFormat):
        self._output_format = value
        if value.media_type == AnyFormat.media_type:
            self.extension = ''
        else:
            self._output_ext = mimetypes.guess_extension(value.media_type) or ''

    @property
    def output_extension(self) -> str:
        return self._output_ext

    @output_extension.setter
    def output_extension(self, ext: str):
        assert_precondition(ext.startswith('.'), "Suffix should start with a '.'")
        self._output_ext = ext
        media_type = mimetypes.types_map.get(ext)
        self._output_format = OutputFormat(media_type=media_type) \
            if media_type else AnyFormat

    def copy_format_from(self, other: Self):
        self._output_format = other._output_format
        self._output_ext = other._output_ext

#
# Input error
#


class InputValueError(Exception):
    pass
