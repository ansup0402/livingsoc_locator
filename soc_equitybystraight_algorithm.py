# -*- coding: utf-8 -*-

"""
/***************************************************************************
 SAOLA
                                 A QGIS plugin
Spatial accessibility and optimal location analysis tool (SAOLA)
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-08-15
        copyright            : (C) 2019 by Ansup
        email                : ansup0402@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Ansup'
__date__ = '2019-08-15'
__copyright__ = '(C) 2019 by Ansup'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       # QgsFeatureSink,
                       QgsVectorLayer,
                       QgsProcessingParameterVectorDestination,
                       QgsProcessingParameterMapLayer,
                       QgsProcessingFeatureSourceDefinition,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProject,
                       QgsProcessingParameterEnum,
                       QgsFeatureRequest,
                       QgsProcessingParameterFeatureSink)

import os
import pathlib
cur_dir = pathlib.Path(__file__).parent
debugging = os.path.exists(os.path.join(cur_dir, 'debugmode'))
if debugging:
    file = open(os.path.join(cur_dir, 'debugmode'), "r")
    cur_dir = file.readline()

class LivingSOCEquityStraightAlgorithm(QgsProcessingAlgorithm):

    IN_CURSOC = 'IN_CURSOC'
    # IN_CURSOC_ID = 'IN_CURSOC_ID'
    IN_LIVINGAREA = 'IN_LIVINGAREA'
    IN_POP = 'IN_POP'
    # IN_LIVINGAREA_ID = 'IN_LIVINGAREA_ID'
    IN_POP_CNTFID = 'IN_POP_CNTFID'
    IN_SITE = 'IN_SITE'


    IN_GRID_SIZE = 'IN_GRID_SIZE'
    IN_LIMIT_DIST = 'IN_LIMIT_DIST'
    IN_CALSSIFYNUM = 'IN_CALSSIFYNUM'
    OUTPUT = 'OUTPUT'


    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.

        # 기존 SOC 시설 레이어
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_CURSOC,
                '❖ ' + self.tr('Located Neighborhood Facility'),
                [QgsProcessing.TypeVectorPoint],
                optional=debugging)
        )

        # 세생활권 인구 레이어
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_LIVINGAREA,
                '❖ ' + self.tr('Sub-Neighborhood Unit'),
                [QgsProcessing.TypeVectorPolygon],
                optional=debugging)
        )

        # 거주 인구 레이어
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_POP,
                '❖ ' + self.tr('Resident Population'),
                [QgsProcessing.TypeVectorPoint],
                optional=debugging)
        )

        # 인구 필드
        self.addParameter(
            QgsProcessingParameterField(
                self.IN_POP_CNTFID,
                self.tr('Population Field'),
                None,
                self.IN_POP,
                QgsProcessingParameterField.Numeric,
                optional=debugging)
        )

        #분석지역
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_SITE,
                '❖ ' + self.tr('Analysis Site'),
                [QgsProcessing.TypeVectorPolygon],
                optional=debugging)
        )
        # 분석 최소단위(잠재적 위치 격자 사이즈)
        self.addParameter(
            QgsProcessingParameterNumber(
                self.IN_GRID_SIZE,
                '❖ ' + self.tr('Analysis Unit(Cell size : m)'),
                QgsProcessingParameterNumber.Integer,
                1000, False, 100, 10000)        #디폴트, 옵션, 미니멈, 맥시멈
        )

        # 거리 조날
        self.addParameter(
            QgsProcessingParameterNumber(
                self.IN_LIMIT_DIST,
                # "❖ " + self.tr('Facility Effective Service Coverage : If you input 0, it is regarded as the whole area'),
                "❖ " + self.tr('Facility Effective Service Coverage'),
                QgsProcessingParameterNumber.Integer,
                1000, False, 0, 1000000)        #디폴트, 옵션, 미니멈, 맥시멈
        )

        # 등급
        self.addParameter(
            QgsProcessingParameterNumber(
                self.IN_CALSSIFYNUM,
                '❖ ' + self.tr('Analysis result grade number of sections: configurable range (2 ~ 100)'),
                QgsProcessingParameterNumber.Integer,
                10, False, 2, 100)  # 디폴트, 옵션, 미니멈, 맥시멈
        )

        # 최종 결과
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT,
                self.tr('Equity Analysis Results(Euclidean)')
            )
        )

    def onlyselectedfeature(self, parameters, context, paramID):
        layersource = self.parameterAsSource(parameters, paramID, context)
        layervertor = self.parameterAsVectorLayer(parameters, paramID, context)
        onlyselectedFeature = (layersource.featureCount() >= 0 and layervertor is None)
        return onlyselectedFeature

    def getLayerfromParameter(self, parameters, context, paramID):
        if self.onlyselectedfeature(parameters, context, paramID):
            return self.parameterAsSource(parameters, paramID, context), True
        else:
            return self.parameterAsSource(parameters, paramID, context), False

    def parameter2Dict(self, parameters, context):
        keyword = {}
        keyword['IN_CURSOC'], keyword['IN_CURSOC_ONLYSELECTED'] = self.getLayerfromParameter(parameters, context, self.IN_CURSOC)
        # keyword['IN_CURSOC_ID'] = self.parameterAsFields(parameters, self.IN_CURSOC_ID, context)[0]

        keyword['IN_LIVINGAREA'], keyword['IN_LIVINGAREA_ONLYSELECTED'] = self.getLayerfromParameter(parameters, context, self.IN_LIVINGAREA)
        # keyword['IN_LIVINGAREA_ID'] = self.parameterAsFields(parameters, self.IN_LIVINGAREA_ID, context)[0]

        keyword['IN_POP'], keyword['IN_POP_ONLYSELECTED'] = self.getLayerfromParameter(parameters, context, self.IN_POP)
        keyword['IN_POP_CNTFID'] = self.parameterAsFields(parameters, self.IN_POP_CNTFID, context)[0]

        keyword['IN_SITE'], keyword['IN_SITE_ONLYSELECTED'] = self.getLayerfromParameter(parameters, context, self.IN_SITE)

        keyword['IN_GRID_SIZE'] = self.parameterAsInt(parameters, self.IN_GRID_SIZE, context)
        keyword['IN_LIMIT_DIST'] = self.parameterAsInt(parameters, self.IN_LIMIT_DIST, context)
        keyword['IN_CALSSIFYNUM'] = self.parameterAsInt(parameters, self.IN_CALSSIFYNUM, context)
        keyword['OUTPUT'] = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        return keyword

    def check_userinput(self, parameters):
        # 사용자가 자주 실수하는 부분 파악하여 해당 함수 완성 할 것(노드, 링크 관계, PK필드 누락 등)
        isvailid = True
        return isvailid


    def processAlgorithm(self, parameters, context, feedback):

        params = self.parameter2Dict(parameters, context)

        # if self.check_userinput(parameters=params) == False: return None

        try:
            from .soc_locator_launcher import soc_locator_launcher
        except ImportError:
            from soc_locator_launcher import soc_locator_launcher

        global debugging
        global cur_dir
        if debugging:
            feedback.pushInfo("****** [START DEBUG] ******")
            feedback.pushInfo(cur_dir)
        launcher = soc_locator_launcher(feedback=feedback, context=context, parameters=params, debugging=debugging,
                                        workpath=cur_dir)

        out_vector = launcher.execute_equity_in_straight()

        return {self.OUTPUT: out_vector}




    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        # return 'Equity Location Model'
        return 'Equity Based Location Analysis(Euclidean)'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        # return 'Life-Friendly SOC Locator'
        # return 'Priority Supply Area Analysis'
        return 'Neighborhood Facility Priority Location Analysis'
    def tr(self, string):
        return QCoreApplication.translate('koala', string)

    def createInstance(self):
        return LivingSOCEquityStraightAlgorithm()

