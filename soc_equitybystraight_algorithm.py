# -*- coding: utf-8 -*-

import os
import pathlib
cur_dir = pathlib.Path(__file__).parent
debugging = os.path.exists(os.path.join(cur_dir, 'debugmode'))

"""
/***************************************************************************
 LivingSOCLocator
                                 A QGIS plugin
 Life-Friendly SOC Locator
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







class LivingSOCEquityStraightAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

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
                self.tr('❖ 기존 생활SOC 시설(POINT)'),
                [QgsProcessing.TypeVectorPoint],
                optional=debugging)
        )

        # # 기존 SOC 시설 ID
        # self.addParameter(
        #     QgsProcessingParameterField(
        #         self.IN_CURSOC_ID,
        #         self.tr('기존 생활SOC 고유 필드'),
        #         None,
        #         self.IN_CURSOC,
        #         QgsProcessingParameterField.Any,
        #         optional=debugging)
        # )

        # 세생활권 인구 레이어
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_LIVINGAREA,
                self.tr('❖ 세생활권(Polygon)'),
                [QgsProcessing.TypeVectorPolygon],
                optional=debugging)
        )

        # # 인구 ID
        # self.addParameter(
        #     QgsProcessingParameterField(
        #         self.IN_LIVINGAREA_ID,
        #         self.tr('세생활권 고유 필드'),
        #         None,
        #         self.IN_LIVINGAREA,
        #         QgsProcessingParameterField.Any,
        #         optional=debugging)
        # )

        # 거주 인구 레이어
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_POP,
                self.tr('❖ 거주인구(POINT)'),
                [QgsProcessing.TypeVectorPoint],
                optional=debugging)
        )

        # 인구 필드
        self.addParameter(
            QgsProcessingParameterField(
                self.IN_POP_CNTFID,
                self.tr('인구수 필드'),
                None,
                self.IN_POP,
                QgsProcessingParameterField.Numeric,
                optional=debugging)
        )

        #분석지역
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_SITE,
                self.tr('❖ 분석 대상지 선택(Polygon)'),
                [QgsProcessing.TypeVectorPolygon],
                optional=debugging)
        )
        # 분석 최소단위(잠재적 위치 격자 사이즈)
        self.addParameter(
            QgsProcessingParameterNumber(
                self.IN_GRID_SIZE,
                self.tr('❖ 최소 분석 크기(Cell size : m)'),
                QgsProcessingParameterNumber.Integer,
                1000, False, 100, 10000)        #디폴트, 옵션, 미니멈, 맥시멈
        )

        # 거리 조날
        self.addParameter(
            QgsProcessingParameterNumber(
                self.IN_LIMIT_DIST,
                self.tr('❖ 유효 서비스 범위(m) : \'0\'을 입력할 경우 유효 서비스 범위를 대상지역 전체로 간주'),
                QgsProcessingParameterNumber.Integer,
                1000, False, 0, 1000000)        #디폴트, 옵션, 미니멈, 맥시멈
        )

        # 등급
        self.addParameter(
            QgsProcessingParameterNumber(
                self.IN_CALSSIFYNUM,
                self.tr('❖ 분석 결과 등급 구간 수 : 설정 가능 구간(2 ~ 100개 구간)'),
                QgsProcessingParameterNumber.Integer,
                10, False, 2, 100)  # 디폴트, 옵션, 미니멈, 맥시멈
        )

        # 최종 결과
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT,
                self.tr('형평성 분석 결과(직선거리)')
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

        # isvailid = False
        #
        #
        #
        # # 한글필드 체크,
        # # 특수필드들 다른 레이어에 중복된것이 있는지 체크
        # # 다른 필드에 NODE_ID 생성할떄 도일한 필드타입으로 int >< double 다름
        # # 링크에 없는 NODE가 있음 -> 노드를 내부적으로 만들어 줄까?? 아님 링크로 만들까? 아님 체크할까???
        # # NODE_ID는 String으로
        # 금칙 필드 ID 지정
        # if networkmode == 0:
        #     pass
        #
        # return isvailid
        pass


    def processAlgorithm(self, parameters, context, feedback):

        params = self.parameter2Dict(parameters, context)

        # if self.check_userinput(parameters=params) == False: return None

        try:
            from .soc_locator_launcher import soc_locator_launcher
        except ImportError:
            from soc_locator_launcher import soc_locator_launcher

        global debugging
        if debugging: feedback.pushInfo("****** [START DEBUG] ******")

        launcher = soc_locator_launcher(feedback=feedback, context=context, parameters=params, debugging=debugging)

        out_vector = launcher.execute_equity_in_straight()

        return {self.OUTPUT: out_vector}



    def testUnit(self):
        pass


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        # return 'Equity Location Model'
        return '형평성 기준 분석(직선거리)'

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
        return '생활SOC 우선검토지역 분석'
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return LivingSOCEquityStraightAlgorithm()

