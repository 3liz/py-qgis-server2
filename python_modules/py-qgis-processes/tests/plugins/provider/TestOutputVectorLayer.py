""" Returns a simple bar chart
"""
import traceback

from pathlib import Path

import processing

from qgis.core import (
    QgsProcessingAlgorithm,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
)


class TestOutputVectorLayer(QgsProcessingAlgorithm):

    INPUT = 'INPUT'
    DISTANCE = 'DISTANCE'
    OUTPUT = 'OUTPUT'

    def __init__(self):
        super().__init__()

    def name(self):
        return 'vectoroutput'

    def displayName(self):
        return 'Vector output test'

    def createInstance(self, config={}):
        """ Virtual override

            see https://qgis.org/api/classQgsProcessingAlgorithm.html
        """
        return self.__class__()

    def initAlgorithm(self, config=None):
        """ Virtual override

            see https://qgis.org/api/classQgsProcessingAlgorithm.html
        """
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                'Input layer',
            ),
        )

        self.addParameter(QgsProcessingParameterNumber(self.DISTANCE, 'Distance',
            type=QgsProcessingParameterNumber.Double, defaultValue=1000))

        self.addOutput(QgsProcessingOutputVectorLayer(self.OUTPUT, "Output"))

    def processAlgorithm(self, parameters, context, feedback):
        try:
            output = str(Path(context.temporaryFolder()).joinpath('my_output_vector.fgb'))

            # Run buffer
            _buffer_result = processing.run("qgis:buffer", {
                'INPUT': parameters[self.INPUT],
                'DISTANCE': parameters[self.DISTANCE],
                'SEGMENTS': 10,
                'END_CAP_STYLE': 0,
                'JOIN_STYLE': 0,
                'MITER_LIMIT': 2,
                'DISSOLVE': False,
                'OUTPUT': output,
            }, context=context, feedback=feedback)

            return {self.OUTPUT: output}

        except Exception:
            traceback.print_exc()