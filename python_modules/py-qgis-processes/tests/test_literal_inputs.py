
from collections import Counter
from datetime import datetime

import pytest

from pydantic import ValidationError
from qgis.core import (
    Qgis,
    QgsProcessingParameterBand,
    QgsProcessingParameterColor,
    QgsProcessingParameterDateTime,
    QgsProcessingParameterDistance,
    QgsProcessingParameterDuration,
    QgsProcessingParameterEnum,
    QgsProcessingParameterField,
    QgsProcessingParameterNumber,
    QgsProcessingParameterRange,
    QgsProcessingParameterScale,
    QgsProcessingParameterString,
)

from py_qgis_processes.processing.inputs import InputParameter
from py_qgis_processes_schemas import ogc


def test_parameter_description():

    param = QgsProcessingParameterString(
        "String",
        description="String description",
    )
    param.setHelp("String help")

    inp = InputParameter(param)

    descr = inp.description()
    assert descr.title == "String description"
    assert descr.description == "String help"


def test_parameter_string():

    param = QgsProcessingParameterString("String")

    inp = InputParameter(param)

    schema = inp.json_schema()

    print("\ntest_parameter_string::", schema)

    assert schema['type'] == 'string'

    with pytest.raises(ValidationError):
        value = inp.value(1)

    value = inp.value("foo")
    assert param.checkValueIsAcceptable(value)


def test_parameter_enum():

    param = QgsProcessingParameterEnum(
        "Enum",
        options=["foo", "bar", "baz"],
        allowMultiple=False,
        defaultValue=1,
    )

    inp = InputParameter(param)

    schema = inp.json_schema()

    print("\ntest_parameter_enum::", schema)

    assert schema['type'] == 'string'
    assert schema['default'] == 'bar'
    assert schema['format'] == 'x-qgis-parameter-enum'

    with pytest.raises(ValidationError):
        value = inp.value("not_an_option")

    value = inp.value("bar")
    assert value == 1

    assert param.checkValueIsAcceptable(value)


def test_parameter_enum_multiple():

    param = QgsProcessingParameterEnum(
        "Enum",
        options=["foo", "bar", "baz"],
        allowMultiple=True,
    )

    inp = InputParameter(param)

    schema = inp.json_schema()

    print("\ntest_parameter_enum_multiple::", schema)

    assert schema['type'] == 'array'

    value = inp.value(["foo", "bar"])
    assert Counter(value) == Counter([0, 1])

    assert param.checkValueIsAcceptable(value)
    assert not param.checkValueIsAcceptable(["foo", "bar"])

    param.setUsesStaticStrings(True)
    value = inp.value(["foo", "bar"])

    print("test_parameter_enum_multiple::", value)

    assert Counter(value) == Counter(["foo", "bar"])
    assert param.checkValueIsAcceptable(value)


def test_parameter_number():

    param = QgsProcessingParameterNumber(
        "Number",
        type=Qgis.ProcessingNumberParameterType.Integer,
    )

    inp = InputParameter(param)

    schema = inp.json_schema()

    print("\ntest_parameter_number::", schema)

    assert schema['type'] == 'integer'

    with pytest.raises(ValidationError):
        value = inp.value("bar")

    value = inp.value(1.)
    print("test_parameter_number::integer value::", value)
    assert param.checkValueIsAcceptable(value)

    param = QgsProcessingParameterNumber(
        "Number",
        type=Qgis.ProcessingNumberParameterType.Double,
        minValue=0.,
        maxValue=1.,
    )

    inp = InputParameter(param)

    schema = inp.json_schema()

    print("\ntest_parameter_number::double::", schema)

    assert schema['type'] == 'number'
    assert schema['maximum'] == 1.0
    assert schema['minimum'] == 0.0


def test_parameter_distance():

    param = QgsProcessingParameterDistance("Distance")
    param.setDefaultUnit(Qgis.DistanceUnit.Meters)

    inp = InputParameter(param)

    schema = inp.json_schema()

    print("\ntest_parameter_distance::", schema)
    assert schema['type'] == 'number'
    assert schema['x-ogc-definition'] == ogc.OgcDataType['length']
    assert schema['x-ogc-uom'] == str(ogc.UOMRef.from_name('m'))


def test_parameter_scale():

    param = QgsProcessingParameterScale("Scale")

    inp = InputParameter(param)

    schema = inp.json_schema()
    print("\ntest_parameter_scale::", schema)
    assert schema['type'] == 'number'
    assert schema['x-ogc-definition'] == ogc.OgcDataType['scale']


def test_parameter_duration():

    param = QgsProcessingParameterDuration("Duration")

    inp = InputParameter(param)

    schema = inp.json_schema()
    print("\ntest_parameter_duration::", schema)
    assert schema['type'] == 'number'
    assert schema['x-ogc-definition'] == ogc.OgcDataType['time']


def test_parameter_range():

    param = QgsProcessingParameterRange("Range")

    inp = InputParameter(param)

    schema = inp.json_schema()
    print("\ntest_parameter_range::", schema)
    assert schema['type'] == 'array'
    assert schema['format'] == 'x-qgis-parameter-range'
    assert schema['maxLength'] == 2
    assert schema['minLength'] == 2


def test_parameter_datetime():

    from qgis.PyQt.QtCore import QDateTime

    qdt = QDateTime.currentDateTime()
    param = QgsProcessingParameterDateTime("DateTime", minValue=qdt)

    inp = InputParameter(param)

    schema = inp.json_schema()
    print("\ntest_parameter_datetime::", schema)
    assert schema['type'] == 'string'
    assert schema['format'] == 'date-time'
    assert schema['formatMinimum'] == qdt.toPyDateTime().isoformat()

    value = inp.value(datetime.now().isoformat())
    assert param.checkValueIsAcceptable(value)

    param = QgsProcessingParameterDateTime("DateTime", maxValue=qdt)
    inp = InputParameter(param)

    with pytest.raises(ValidationError):
        value = inp.value(datetime.now().isoformat())

    param = QgsProcessingParameterDateTime(
        "DateTime",
        type=Qgis.ProcessingDateTimeParameterDataType.Date,
    )
    inp = InputParameter(param)
    schema = inp.json_schema()
    assert schema['format'] == 'date'

    param = QgsProcessingParameterDateTime(
        "DateTime",
        type=Qgis.ProcessingDateTimeParameterDataType.Time,
    )
    inp = InputParameter(param)
    schema = inp.json_schema()
    assert schema['format'] == 'time'


def test_parameter_band():

    param = QgsProcessingParameterBand("Band")

    inp = InputParameter(param)

    schema = inp.json_schema()
    print("\ntest_parameter_band::", schema)
    assert schema['type'] == 'integer'
    assert schema['minimum'] == 0
    assert schema['format'] == 'x-qgis-parameter-band'

    param = QgsProcessingParameterBand("Band", allowMultiple=True)
    inp = InputParameter(param)
    schema = inp.json_schema()
    print("\ntest_parameter_band::multiple", schema)
    assert schema['type'] == 'array'


def test_parameter_color():

    from qgis.PyQt.QtGui import QColor

    param = QgsProcessingParameterColor("Color", defaultValue=QColor(0, 0, 255, 128))

    inp = InputParameter(param)

    schema = inp.json_schema()
    print("\ntest_parameter_color::", schema)
    assert schema['type'] == 'string'
    assert schema['format'] == 'color'
    assert schema['default'] == '#0000ff80'

    value = inp.value("red")
    assert value == QColor(255, 0, 0)


def test_parameter_field():

    param = QgsProcessingParameterField(
        "Field",
        parentLayerParameterName="ParentLayer",
        type=Qgis.ProcessingFieldParameterDataType.Numeric,
    )

    inp = InputParameter(param)

    schema = inp.json_schema()
    print("\ntest_parameter_field::", schema)
    assert schema['type'] == 'string'
    assert schema['format'] == 'x-qgis-parameter-field'
    assert schema['x-qgis-parentLayerParameterName'] == 'ParentLayer'
    assert schema['x-qgis-field-dataType'] == 'Numeric'

    param = QgsProcessingParameterField("Field", allowMultiple=True)
    inp = InputParameter(param)
    schema = inp.json_schema()
    print("\ntest_parameter_field::multiple", schema)
    assert schema['type'] == 'array'
    assert schema['minItems'] == 1