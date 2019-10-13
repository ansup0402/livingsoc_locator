# -*- coding: utf-8 -*-
import os
import pathlib
cur_dir = pathlib.Path(__file__).parent
debugging = os.path.exists(os.path.join(cur_dir, 'debugmode'))

# debugging = False

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
                       QgsProcessingParameterVectorDestination,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProject,
                       QgsProcessingParameterString,
                       QgsProcessingParameterFeatureSink)


class LivingSOCAccessibilitynetworkAlgorithm(QgsProcessingAlgorithm):
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
    IN_LIVINGAREA = 'IN_LIVINGAREA'
    # IN_LIVINGAREA_ID = 'IN_LIVINGAREA_ID'

    IN_POP = 'IN_POP'
    # IN_POP_ID = 'IN_POP_ID'
    IN_POP_CNTFID = 'IN_POP_CNTFID'
    IN_SITE = 'IN_SITE'
    # IN_NETWORK_MODE = 'IN_NETWORK_MODE'
    IN_NODE = 'IN_NODE'
    IN_NODE_ID = 'IN_NODE_ID'
    IN_LINK = 'IN_LINK'
    IN_LINK_TYPE = 'IN_LINK_TYPE'
    IN_LINK_FNODE = 'IN_LINK_FNODE'
    IN_LINK_TNODE = 'IN_LINK_TNODE'
    IN_LINK_LENGTH = 'IN_LINK_LENGTH'
    IN_LINK_SPEED = 'IN_LINK_SPEED'
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

        # 세생활권 인구 레이어
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_LIVINGAREA,
                self.tr('❖ 세생활권(Polygon)'),
                [QgsProcessing.TypeVectorPolygon],
                optional=debugging)
        )

        # # 세생활권 ID
        # self.addParameter(
        #     QgsProcessingParameterField(
        #         self.IN_LIVINGAREA_ID,
        #         self.tr('세생활권 고유 필드'),
        #         None,
        #         self.IN_LIVINGAREA,
        #         QgsProcessingParameterField.Any,
        #         optional=debugging)
        # )


        # 세생활권 인구 레이어
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_POP,
                self.tr('❖ 거주 인구(POINT)'),
                [QgsProcessing.TypeVectorPoint],
                optional=debugging)
        )

        # # 세생활권 ID
        # self.addParameter(
        #     QgsProcessingParameterField(
        #         self.IN_POP_ID,
        #         self.tr('거주인구 고유 필드'),
        #         None,
        #         self.IN_POP,
        #         QgsProcessingParameterField.Any,
        #         optional=debugging)
        # )



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

        # 분석지역
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_SITE,
                self.tr('❖ 분석 영역 선택(Polygon)'),
                [QgsProcessing.TypeVectorPolygon],
                optional=debugging)
        )


        # 거리 조락
        self.addParameter(
            QgsProcessingParameterNumber(
                self.IN_LIMIT_DIST,
                self.tr('❖ 유효 서비스 범위(m) : \'0\'을 입력할 경우 유효 서비스 범위를 대상지역 전체로 간주'),
                QgsProcessingParameterNumber.Integer,
                1000, False, 0, 1000000)  # 디폴트, 옵션, 미니멈, 맥시멈
        )

        # 노드레이어
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_NODE,
                self.tr('노드 레이어(POINT)'),
                [QgsProcessing.TypeVectorPoint],
                optional=debugging)
        )
        # 노드레이어 PK
        self.addParameter(
            QgsProcessingParameterField(
                self.IN_NODE_ID,
                self.tr('노드ID 필드'),
                None,
                self.IN_NODE,
                QgsProcessingParameterField.Any,
                optional=debugging)
        )

        # 링크레이어
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.IN_LINK,
                self.tr('❖ 링크 레이어(LINE)'),
                [QgsProcessing.TypeVectorLine],
                optional=debugging)
        )

        self.addParameter(
            QgsProcessingParameterEnum(
                self.IN_LINK_TYPE,
                self.tr('링크 레이어 유형'),
                options=[self.tr('단방향'), self.tr('양방향')],
                defaultValue=1,
                optional=debugging)
        )

        # 기점 노드 필드
        self.addParameter(
            QgsProcessingParameterField(
                self.IN_LINK_FNODE,
                self.tr('기점 노드 필드'),
                None,
                self.IN_LINK,
                QgsProcessingParameterField.Any,
                optional=debugging)
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.IN_LINK_TNODE,
                self.tr('종점 노드 필드'),
                None,
                self.IN_LINK,
                QgsProcessingParameterField.Any,
                optional=debugging)
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.IN_LINK_LENGTH,
                self.tr('링크 길이 필드'),
                None,
                self.IN_LINK,
                QgsProcessingParameterField.Numeric,
                optional=debugging)
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.IN_LINK_SPEED,
                self.tr('속도 필드'),
                None,
                self.IN_LINK,
                QgsProcessingParameterField.Numeric,
                optional=True)
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
                self.tr('접근성 분석 결과(네트워크)')
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


        keyword['IN_LIVINGAREA'], keyword['IN_LIVINGAREA_ONLYSELECTED'] = self.getLayerfromParameter(parameters, context, self.IN_LIVINGAREA)
        # keyword['IN_LIVINGAREA_ID'] = self.parameterAsFields(parameters, self.IN_LIVINGAREA_ID, context)[0]

        keyword['IN_POP'], keyword['IN_POP_ONLYSELECTED'] = self.getLayerfromParameter(parameters, context, self.IN_POP)
        # keyword['IN_POP_ID'] = self.parameterAsFields(parameters, self.IN_POP_ID, context)[0]
        keyword['IN_POP_CNTFID'] = self.parameterAsFields(parameters, self.IN_POP_CNTFID, context)[0]

        keyword['IN_SITE'], keyword['IN_SITE_ONLYSELECTED'] = self.getLayerfromParameter(parameters, context, self.IN_SITE)

        keyword['IN_NODE'], keyword['IN_NODE_ONLYSELECTED'] = self.getLayerfromParameter(parameters, context, self.IN_NODE)
        keyword['IN_NODE_ID'] = self.parameterAsFields(parameters, self.IN_NODE_ID, context)[0]

        keyword['IN_LINK'], keyword['IN_LINK_ONLYSELECTED'] = self.getLayerfromParameter(parameters, context, self.IN_LINK)
        keyword['IN_LINK_TYPE'] = self.parameterAsEnum(parameters, self.IN_LINK_TYPE, context)  # 0:단방향, 1:양방향
        keyword['IN_LINK_FNODE'] = self.parameterAsFields(parameters, self.IN_LINK_FNODE, context)[0]
        keyword['IN_LINK_TNODE'] = self.parameterAsFields(parameters, self.IN_LINK_TNODE, context)[0]
        keyword['IN_LINK_LENGTH'] = self.parameterAsFields(parameters, self.IN_LINK_LENGTH, context)[0]

        if len(self.parameterAsFields(parameters, self.IN_LINK_SPEED, context)) == 0:
            keyword['IN_LINK_SPEED'] = None
        else:
            keyword['IN_LINK_SPEED'] = self.parameterAsFields(parameters, self.IN_LINK_SPEED, context)[0]

        keyword['IN_LIMIT_DIST'] = self.parameterAsInt(parameters, self.IN_LIMIT_DIST, context)
        keyword['IN_CALSSIFYNUM'] = self.parameterAsInt(parameters, self.IN_CALSSIFYNUM, context)
        keyword['OUTPUT'] = self.parameterAsOutputLayer(parameters, self.OUTPUT, context)

        return keyword


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

        out_vector = launcher.execute_accessbillity_in_network()

        return {self.OUTPUT: out_vector}


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        # return 'Accessibility Analysis Model'
        return '접근성 분석(네트워크거리)'

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
        return '생활SOC 접근성 분석'
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return LivingSOCAccessibilitynetworkAlgorithm()


