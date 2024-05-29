
from pathlib import Path
from urllib.parse import urlsplit

from pydantic import BaseModel, Extra, Field, JsonValue
from typing_extensions import (
    Annotated,
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Set,
    TypeAlias,
)

from qgis.core import (
    Qgis,
    QgsMapLayer,
    QgsProcessingFeatureSourceDefinition,
    QgsProcessingOutputLayerDefinition,
    QgsProcessingParameterBand,
    QgsProcessingParameterExpression,
    QgsProcessingParameterField,
    QgsProcessingParameterFieldMapping,
    QgsProcessingParameterLimitedDataTypes,
    QgsProcessingUtils,
    QgsProject,
)

from py_qgis_processes_schemas.models import (
    NullField,
    OutputFormatDefinition,
)

from ..utils import (
    ProcessingSourceType,
    compatible_layers,
    get_valid_filename,
    parse_layer_spec,
    raw_destination_sink,
)
from .base import (
    InputParameter,
    Metadata,
    MetadataValue,
    ParameterDefinition,
    ProcessingContext,
)

#
# Layers input may be passed in various forms:
#
#    - For input layers and if a context is given: it will be a list of available layers from
#      the source project as literal string.
#
#    We treat layer destination the same as input since they refer to
#    layers ids in qgisProject
#


class ParameterMapLayer(InputParameter):

    _multiple: bool = False

    @classmethod
    def compatible_layers(
        cls,
        param: ParameterDefinition,
        project: QgsProject,
    ) -> Iterable[QgsMapLayer]:
        if isinstance(param, QgsProcessingParameterLimitedDataTypes):
            dtypes = param.dataTypes()
        else:
            dtypes = ()

        return compatible_layers(project, dtypes)

    @classmethod
    def create_model(
        cls,
        param: ParameterDefinition,
        field: Dict,
        project: Optional[QgsProject] = None,
        validation_only: bool = False,
    ) -> TypeAlias:

        _type: Any = str

        if project:
            allowed_sources = tuple(layer.name() for layer in cls.compatible_layers(param, project))
            if allowed_sources:
                _type = Literal[allowed_sources]

        if cls._multiple:
            _type = Set[_type]

        return _type

    def value(
        self,
        inp: JsonValue,
        context: Optional[ProcessingContext] = None,
    ) -> JsonValue:

        _inp = self.validate(inp)
        if self._multiple:
            _inp = [parse_layer_spec(s)[0] for s in _inp]
        else:
            _inp = parse_layer_spec(_inp)[0]

        return _inp


#
# QgsProcessingParameterMultipleLayers
#

class ParameterMultipleLayers(ParameterMapLayer):
    _multiple = True

    @classmethod
    def compatible_layers(
        cls,
        param: ParameterDefinition,
        project: QgsProject,
    ) -> Iterable[QgsMapLayer]:
        return compatible_layers(project, (param.layerType(),))

    @classmethod
    def create_model(
        cls,
        param: ParameterDefinition,
        field: Dict,
        project: Optional[QgsProject] = None,
        validation_only: bool = False,
    ) -> TypeAlias:

        _type = super(ParameterMultipleLayers, cls).create_model(param, field, project, validation_only)

        min_number = param.minimumNumberInputs()
        if min_number > 0:
            field.update(min_length=min_number)

        return _type
#
# QgsProcessingParameterVectorLayer
#


class ParameterVectorLayer(ParameterMapLayer):
    @classmethod
    def compatible_layers(
        cls,
        param: ParameterDefinition,
        project: QgsProject,
    ) -> Iterable[QgsMapLayer]:
        return QgsProcessingUtils.compatibleVectorLayers(project, param.dataTypes())


#
# QgsProcessingParameterFeatureSource
#

class ParameterFeatureSource(ParameterMapLayer):

    @classmethod
    def compatible_layers(
        cls,
        param: ParameterDefinition,
        project: QgsProject,
    ) -> Iterable[QgsMapLayer]:
        return QgsProcessingUtils.compatibleVectorLayers(project, param.dataTypes())

    def value(
        self,
        inp: JsonValue,
        context: Optional[ProcessingContext] = None,
    ) -> QgsProcessingFeatureSourceDefinition:

        #
        # Support feature selection
        #
        _inp = self.validate(inp)

        value, has_selection = parse_layer_spec(_inp, context, allow_selection=True)
        value = QgsProcessingFeatureSourceDefinition(value, selectedFeaturesOnly=has_selection)

        return value

#
# QgsProcessingParameterRasterLayer
#


class ParameterRasterLayer(ParameterMapLayer):
    @classmethod
    def compatible_layers(
        cls,
        param: ParameterDefinition,
        project: QgsProject,
    ) -> Iterable[QgsMapLayer]:
        return QgsProcessingUtils.compatibleRasterLayers(project)


#
# QgsProcessingParameterPointCloudLayer
#

class ParameterPointCloudLayer(ParameterMapLayer):
    @classmethod
    def compatible_layers(
        cls,
        param: ParameterDefinition,
        project: QgsProject,
    ) -> Iterable[QgsMapLayer]:
        return QgsProcessingUtils.compatiblePointCloudLayers(project)


#
# QgsProcessingParameterVectorTileWriterLayers
#

class ParameterVectorTileWriterLayers(ParameterMapLayer):

    @classmethod
    def create_model(
        cls,
        param: ParameterDefinition,
        field: Dict,
        project: Optional[QgsProject] = None,
        validation_only: bool = False,
    ) -> TypeAlias:

        _type: Any = super(ParameterVectorTileWriterLayers, cls).create_model(
            param,
            field,
            project,
            validation_only,
        )

        # Inputs are List of dict
        # Build intermediate representation for
        # enforcing constraints
        class TileWriter(BaseModel, extra=Extra.allow):
            layer: _type

        return Sequence[TileWriter]

    def value(self, inp: JsonValue, context: Optional[ProcessingContext] = None) -> Dict:
        _inp = self.validate(inp)
        return self._model.dump_python(_inp, mode='json', by_alias=True, exclude_none=True)


#
# QgsProcessingParameterDxfLayers
#

class ParameterDxfLayers(ParameterMapLayer):
    _multiple: bool = True

    @classmethod
    def compatible_layers(
        cls,
        param: ParameterDefinition,
        project: QgsProject,
    ) -> Iterable[QgsMapLayer]:
        return (layer for layer in QgsProcessingUtils.compatibleVectorLayers(project)
                    if layer.isSpatial())


#
# QgsProcessingParameterAnnotationLayer
#

class ParameterAnnotationLayer(ParameterMapLayer):
    @classmethod
    def compatible_layers(cls, param: ParameterDefinition, project: QgsProject) -> Sequence[str]:
        return QgsProcessingUtils.compatibleAnnotationLayers(project)


#
# QgsProcessingParameterTinInputLayers
#

class ParameterTinInputLayers(ParameterMapLayer):
    _multiple = True

    @classmethod
    def compatible_layers(cls, param: ParameterDefinition, project: QgsProject) -> Sequence[str]:
        return QgsProcessingUtils.compatibleVectorLayer(project)

    @classmethod
    def create_model(
        cls,
        param: ParameterDefinition,
        field: Dict,
        project: Optional[QgsProject] = None,
        validation_only: bool = False,
    ) -> TypeAlias:

        _type: Any = super(ParameterTinInputLayers, cls).create_model(
            param,
            field,
            project,
            validation_only,
        )

        # Inputs are List of dict
        # Build intermediate representation for
        # enforcing constraints
        class TinInput(BaseModel, extra='allow'):
            source: _type
            attributeIndex: str
            type_: str = Field(alias="type")

        return Sequence[TinInput]

    def value(self, inp: JsonValue, context: Optional[ProcessingContext] = None) -> Dict:
        _inp = self.validate(inp)
        return self._model.dump_python(_inp, mode='json', by_alias=True, exclude_none=True)

#
# Layer destination
#


class ParameterLayerDestination(InputParameter, OutputFormatDefinition):

    def initialize(self):
        self.output_extension = f".{self._param.defaultFileExtension()}"

    @classmethod
    def get_default_value(cls, field: Dict, param: ParameterDefinition) -> str:
        #
        # Get the file extension as we need it
        # for writing the resulting file
        #
        defval = field.pop('default', None)

        if isinstance(defval, QgsProcessingOutputLayerDefinition):
            sink = defval.sink and defval.sink.staticValue()
            if sink:
                # Remove extra open options
                url = urlsplit(sink.partition('|')[0])
                if url.path and url.scheme.lower() in ('', 'file'):
                    p = Path(url.path)
                    defval = defval.destinationName or p.stem

        return defval

    @classmethod
    def create_model(
        cls,
        param: ParameterDefinition,
        field: Dict,
        project: Optional[QgsProject] = None,
        validation_only: bool = False,
    ) -> TypeAlias:

        _type = str

        if not validation_only:
            # Since QgsProcessingOutputLayerDefinition may
            # be defined as default value, get layer name from it
            defval = cls.get_default_value(field, param)
            if defval:
                field.update(default=defval)

        return _type

    def value(
        self,
        inp: JsonValue,
        context: Optional[ProcessingContext] = None,
    ) -> QgsProcessingOutputLayerDefinition:

        context = context or ProcessingContext()

        destination = self.validate(inp)
        extension = self.output_extension

        if context.config.raw_destination_input_sink:
            sink, destination = raw_destination_sink(
                self._param,
                destination,
                context.workdir,
                extension,
                context.config.raw_destination_root_path,
            )
        else:
            #
            # Destination layer: a new layer is created as file with the input name.
            # Do not supports memory layer because we need persistence
            #
            self._param.setSupportsNonFileBasedOutput(False)
            #
            # Enforce pushing created layers to layersToLoadOnCompletion list
            # i.e layer will be stored in the destination project

            output_name = get_valid_filename(self._param.name())
            # Use canonical file name
            sink = str(context.workdir.joinpath(f"{output_name}{extension}"))

        destination_project = context.destination_project

        value = QgsProcessingOutputLayerDefinition(sink, destination_project)
        value.destinationName = destination

        return value


#
# QgsProcessingParameterRasterDestination
#

class ParameterRasterDestination(ParameterLayerDestination):
    pass

#
# QgsProcessingParameterVectorDestination
#


class ParameterVectorDestination(ParameterLayerDestination):

    @classmethod
    def metadata(cls, param: QgsProcessingParameterField) -> List[Metadata]:
        md = super(ParameterVectorDestination, cls).metadata(param)
        md.append(
            MetadataValue(
                role="dataType",
                value=ProcessingSourceType(param.dataType()).name,
            ),
        )
        return md

    @classmethod
    def create_model(
        cls,
        param: ParameterDefinition,
        field: Dict,
        project: Optional[QgsProject] = None,
        validation_only: bool = False,
    ) -> TypeAlias:

        _type = super(ParameterVectorDestination, cls).create_model(
            param,
            field,
            project,
            validation_only,
        )

        if not validation_only:
            schema_extra = field.get('json_schema_extra', {})
            field.update(json_schema_extra=schema_extra)

        return _type


#
# QgsProcessingParameterFeatureSink
#

class ParameterFeatureSink(ParameterVectorDestination):
    pass


#
# QgsProcessingPointCloudDestination
#

class ParameterPointCloudDestination(ParameterLayerDestination):
    pass


#
# QgsProcessingVectorTileDestination
#

class ParameterVectorTileDestination(ParameterLayerDestination):
    pass


#
# QgsProcessingParameterField
#

if Qgis.QGIS_VERSION_INT >= 33600:
    FieldParameterDataType = Qgis.ProcessingFieldParameterDataType
    def field_datatype_name(value: Qgis.ProcessingFieldParameterDataType) -> str:
        return value.name
else:
    FieldParameterDataType = QgsProcessingParameterField
    def field_datatype_name(value: int) -> str:   # type: ignore [misc]
        match value:
            case QgsProcessingParameterField.Any:
                field_datatype = 'Any'
            case QgsProcessingParameterField.Numeric:
                field_datatype = 'Numeric'
            case QgsProcessingParameterField.String:
                field_datatype = 'String'
            case QgsProcessingParameterField.DateTime:
                field_datatype = 'DateTime'
            case QgsProcessingParameterField.Binary:
                field_datatype = 'Binary'
            case QgsProcessingParameterField.Boolean:
                field_datatype = 'Boolean'
            case _:
                raise ValueError(f"Unexpected field_datatype: {value}")
        return field_datatype


class ParameterField(InputParameter):

    @classmethod
    def metadata(cls, param: QgsProcessingParameterField) -> List[Metadata]:
        md = super(ParameterField, cls).metadata(param)
        md.append(MetadataValue(role="dataType", value=field_datatype_name(param.dataType())))
        md.append(MetadataValue(role="defaultToAllFields", value=param.defaultToAllFields()))

        parent_layer_param = param.parentLayerParameterName()
        if parent_layer_param:
            md.append(
                MetadataValue(
                    role="parentLayerParameterName",
                    value=parent_layer_param,
                ),
            )

        return md

    @classmethod
    def create_model(
        cls,
        param: QgsProcessingParameterField,
        field: Dict,
        project: Optional[QgsProject] = None,
        validation_only: bool = False,
    ) -> TypeAlias:

        _type: Any = str  #

        if param.allowMultiple():
            _type = Annotated[List[_type], Field(min_length=1)]  # type: ignore [misc]

        return _type

#
# QgsProcessingParameterFieldMapping
#


class FieldMapping(BaseModel, extra='allow'):
    name: str
    type_: str = Field(alias="type")
    expression: str


class ParameterFieldMapping(InputParameter):

    @classmethod
    def metadata(cls, param: QgsProcessingParameterFieldMapping) -> List[Metadata]:
        md = super(ParameterFieldMapping, cls).metadata(param)
        parent_layer_param = param.parentLayerParameterName()
        if parent_layer_param:
            md.append(
                MetadataValue(
                    role="parentLayerParameterName",
                    value=parent_layer_param,
                ),
            )

        return md

    @classmethod
    def create_model(
        cls,
        param: QgsProcessingParameterField,
        field: Dict,
        project: Optional[QgsProject] = None,
        validation_only: bool = False,
    ) -> TypeAlias:

        return Sequence[FieldMapping]

    def value(self, inp: JsonValue, context: Optional[ProcessingContext] = None) -> Dict:
        _inp = self.validate(inp)
        return self._model.dump_python(_inp, mode='json', by_alias=True, exclude_none=True)


#
# QgisProcessingParameterExpression
#

class ParameterExpression(InputParameter):
    _ParameterType = str

    @classmethod
    def metadata(cls, param: QgsProcessingParameterExpression) -> List[Metadata]:
        md = super(ParameterExpression, cls).metadata(param)
        md.append(MetadataValue(role="expressionType", value=param.expressionType().name))
        parent_layer_parameter = param.parentLayerParameterName()
        if parent_layer_parameter:
            md.append(
                MetadataValue(
                    role="parentLayerParameterName",
                    value=parent_layer_parameter,
                ),
            )

        return md


#
# QgsProcessingParameterBand
#

class ParameterBand(InputParameter):

    @classmethod
    def metadata(cls, param: ParameterDefinition) -> List[Metadata]:
        md = super(ParameterBand, cls).metadata(param)
        parent_layer_param = param.parentLayerParameterName()
        if parent_layer_param:
            md.append(
                MetadataValue(
                    role="parentLayerParameterName",
                    value=parent_layer_param,
                ),
            )

        return md

    @classmethod
    def create_model(
        cls,
        param: QgsProcessingParameterBand,
        field: Dict,
        project: Optional[QgsProject] = None,
        validation_only: bool = False,
    ) -> TypeAlias:

        _type: Any = Annotated[int, Field(ge=0)]  #

        if param.allowMultiple():
            _type = Annotated[List[_type], Field(min_length=1)]  # type: ignore [misc]

        return _type


#
# QgsProcessingParameterAggregate
#

# See analyzing/processing/qgsalgorithmaggregate.cpp
class AggregateItem(BaseModel, extra='allow'):
    name: str
    type_: str = Field(alias='type')
    type_name: Optional[str] = NullField()
    sub_type: Optional[int] = NullField()
    input_: str = Field(alias='input')
    aggregate: str
    length: Optional[int] = NullField()
    precision: Optional[int] = NullField()
    delimiter: Optional[str] = NullField()


class ParameterAggregate(InputParameter):
    _ParameterType = Sequence[AggregateItem]

    @classmethod
    def metadata(cls, param: ParameterDefinition) -> List[Metadata]:
        md = super(ParameterAggregate, cls).metadata(param)
        parent_layer_param = param.parentLayerParameterName()
        if parent_layer_param:
            md.append(
                MetadataValue(
                    role="parentLayerParameterName",
                    value=parent_layer_param,
                ),
            )

        return md

    def value(self, inp: JsonValue, context: Optional[ProcessingContext] = None) -> Dict:
        _inp = self.validate(inp)
        return self._model.dump_python(_inp, mode='json', by_alias=True, exclude_none=True)


#
# QgsProcessingParameterAlignRasterLayers
#


class ParameterAlignRasterLayers(InputParameter):

    @classmethod
    def compatible_layers(
        cls,
        param: ParameterDefinition,
        project: QgsProject,
    ) -> Iterable[QgsMapLayer]:
        return QgsProcessingUtils.compatibleRasterLayers(project)

    @classmethod
    def create_model(
        cls,
        param: QgsProcessingParameterField,
        field: Dict,
        project: Optional[QgsProject] = None,
        validation_only: bool = False,
    ) -> TypeAlias:

        _type: Any = str
        if project:
            allowed_layers = tuple(layer.name() for layer in cls.compatible_layers(param, project))
            if allowed_layers:
                _type = Literal[allowed_layers]  # type: ignore [valid-type]

        class AlignRasterItem(BaseModel):
            inputFile: _type
            outputFile: str
            resampleMethod: int

        return Sequence[_type] | Sequence[AlignRasterItem]  # type: ignore [return-value]

    def value(self, inp: JsonValue, context: Optional[ProcessingContext] = None) -> Dict:
        _inp = self.validate(inp)
        return self._model.dump_python(_inp, mode='json', by_alias=True, exclude_none=True)
