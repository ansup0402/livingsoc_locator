# -*- coding: utf-8 -*-

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

from qgis.PyQt.QtCore import QSettings, QCoreApplication, QTranslator, qVersion
from qgis.core import QgsProcessingProvider
from .soc_equitybynetwork_algorithm import LivingSOCEquityNetworkAlgorithm
from .soc_equitybystraight_algorithm import LivingSOCEquityStraightAlgorithm

from .soc_accessibilitynetwork_algorithm import LivingSOCAccessibilitynetworkAlgorithm
from .soc_accessibilitystraight_algorithm import LivingSOCAccessibilitystraightAlgorithm

from .soc_efficiencylocatornetwork_algorithm import LivingSOCEfficiencynetworkAlgorithm
from .soc_efficiencylocatorstraight_algorithm import LivingSOCEfficiencystraightAlgorithm

import os

class LivingSOCLocatorProvider(QgsProcessingProvider):

    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)

        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            os.path.dirname(__file__),
            'i18n',
            'koala_{}.qm'.format(locale))

        self.translator = None
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

        if qVersion() > '4.3.3':
            QCoreApplication.installTranslator(self.translator)

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        self.addAlgorithm(LivingSOCEquityNetworkAlgorithm())
        self.addAlgorithm(LivingSOCEquityStraightAlgorithm())

        self.addAlgorithm(LivingSOCAccessibilitynetworkAlgorithm())
        self.addAlgorithm(LivingSOCAccessibilitystraightAlgorithm())

        self.addAlgorithm(LivingSOCEfficiencynetworkAlgorithm())
        self.addAlgorithm(LivingSOCEfficiencystraightAlgorithm())
        # add additional algorithms here
        # self.addAlgorithm(MyOtherAlgorithm())

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'LivingSOCAnalysisModel'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        # return self.tr('Life-Friendly SOC Analysis Model')
        return self.tr('Neighborhood Facility Analysis Toolkit(KoALA)')

    def tr(self, string):
        return QCoreApplication.translate('koala', string)

    def icon(self):
        """
        Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        return QgsProcessingProvider.icon(self)

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
