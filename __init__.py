# -*- coding: utf-8 -*-
"""
/***************************************************************************
 UnnecessaryActivityTracker
                                 A QGIS plugin
 Tracks unnecessary movement using locational data and OSM tags.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-03-25
        copyright            : (C) 2020 by Maximilian Herzog
        email                : maxi.herzog@t-online.de
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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load UnnecessaryActivityTracker class from file UnnecessaryActivityTracker.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .unnecessary_activity_tracker import UnnecessaryActivityTracker
    return UnnecessaryActivityTracker(iface)