# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PacSafe
                                 A QGIS plugin
 PacSAFE produces realistic natural hazard impact scenarios for better planning, preparedness and response activities for Pacific Countries
                             -------------------
        begin                : 2015-03-29
        copyright            : (C) 2015 by Secretariat of the Pacific Community
        email                : sachindras@spc.int
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

#import resources
#import resources_rc
from qgis.core import *

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PacSafe class from file PacSafe.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    QGis.QGIS_RELEASE_NAME = "PacSafe"
    #
    from .PacSafe import PacSafe
    return PacSafe(iface)
