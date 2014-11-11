# -*- coding: utf-8 -*-
"""
/***************************************************************************
 spatialJoin
                                 A QGIS plugin
 spatialJoin
                             -------------------
        begin                : 2014-11-11
        copyright            : (C) 2014 by Enrico Ferreguti
        email                : enricofer@gmail.com
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

def classFactory(iface):
    # load spatialJoin class from file spatialJoin
    from spatialjoin import spatialJoin
    return spatialJoin(iface)
