# -*- coding: utf-8 -*-
"""QGIS Unit tests for QgsComposerMap.

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
__author__ = '(C) 2012 by Dr. Horst Düster / Dr. Marco Hugentobler'
__date__ = '20/08/2012'
__copyright__ = 'Copyright 2012, The QGIS Project'
# This will get replaced with a git SHA1 when you do a git archive
__revision__ = '$Format:%H$'

import qgis  # NOQA

import os

from qgis.PyQt.QtCore import QFileInfo
from qgis.PyQt.QtXml import QDomDocument
from qgis.PyQt.QtGui import QPainter

from qgis.core import (QgsComposerMap,
                       QgsRectangle,
                       QgsRasterLayer,
                       QgsVectorLayer,
                       QgsComposition,
                       QgsMapSettings,
                       QgsProject,
                       QgsMultiBandColorRenderer,
                       QgsCoordinateReferenceSystem
                       )

from qgis.testing import start_app, unittest
from utilities import unitTestDataPath
from qgscompositionchecker import QgsCompositionChecker

start_app()
TEST_DATA_DIR = unitTestDataPath()


class TestQgsComposerMap(unittest.TestCase):

    def __init__(self, methodName):
        """Run once on class initialization."""
        unittest.TestCase.__init__(self, methodName)
        myPath = os.path.join(TEST_DATA_DIR, 'rgb256x256.png')
        rasterFileInfo = QFileInfo(myPath)
        self.raster_layer = QgsRasterLayer(rasterFileInfo.filePath(),
                                           rasterFileInfo.completeBaseName())
        rasterRenderer = QgsMultiBandColorRenderer(
            self.raster_layer.dataProvider(), 1, 2, 3)
        self.raster_layer.setRenderer(rasterRenderer)

        myPath = os.path.join(TEST_DATA_DIR, 'points.shp')
        vector_file_info = QFileInfo(myPath)
        self.vector_layer = QgsVectorLayer(vector_file_info.filePath(),
                                           vector_file_info.completeBaseName(), 'ogr')
        assert self.vector_layer.isValid()

        # pipe = mRasterLayer.pipe()
        # assert pipe.set(rasterRenderer), 'Cannot set pipe renderer'
        QgsProject.instance().addMapLayers([self.raster_layer, self.vector_layer])

        # create composition with composer map
        self.mComposition = QgsComposition(QgsProject.instance())
        self.mComposition.setPaperSize(297, 210)
        self.mComposerMap = QgsComposerMap(self.mComposition, 20, 20, 200, 100)
        self.mComposerMap.setFrameEnabled(True)
        self.mComposerMap.setLayers([self.raster_layer])
        self.mComposition.addComposerMap(self.mComposerMap)

    def testOverviewMap(self):
        overviewMap = QgsComposerMap(self.mComposition, 20, 130, 70, 70)
        overviewMap.setFrameEnabled(True)
        overviewMap.setLayers([self.raster_layer])
        self.mComposition.addComposerMap(overviewMap)
        # zoom in
        myRectangle = QgsRectangle(96, -152, 160, -120)
        self.mComposerMap.setNewExtent(myRectangle)
        myRectangle2 = QgsRectangle(0, -256, 256, 0)
        overviewMap.setNewExtent(myRectangle2)
        overviewMap.overview().setFrameMap(self.mComposerMap.id())
        checker = QgsCompositionChecker('composermap_overview', self.mComposition)
        checker.setControlPathPrefix("composer_mapoverview")
        myTestResult, myMessage = checker.testComposition()
        self.mComposition.removeComposerItem(overviewMap)
        assert myTestResult, myMessage

    def testOverviewMapBlend(self):
        overviewMap = QgsComposerMap(self.mComposition, 20, 130, 70, 70)
        overviewMap.setFrameEnabled(True)
        overviewMap.setLayers([self.raster_layer])
        self.mComposition.addComposerMap(overviewMap)
        # zoom in
        myRectangle = QgsRectangle(96, -152, 160, -120)
        self.mComposerMap.setNewExtent(myRectangle)
        myRectangle2 = QgsRectangle(0, -256, 256, 0)
        overviewMap.setNewExtent(myRectangle2)
        overviewMap.overview().setFrameMap(self.mComposerMap.id())
        overviewMap.overview().setBlendMode(QPainter.CompositionMode_Multiply)
        checker = QgsCompositionChecker('composermap_overview_blending', self.mComposition)
        checker.setControlPathPrefix("composer_mapoverview")
        myTestResult, myMessage = checker.testComposition()
        self.mComposition.removeComposerItem(overviewMap)
        assert myTestResult, myMessage

    def testOverviewMapInvert(self):
        overviewMap = QgsComposerMap(self.mComposition, 20, 130, 70, 70)
        overviewMap.setFrameEnabled(True)
        overviewMap.setLayers([self.raster_layer])
        self.mComposition.addComposerMap(overviewMap)
        # zoom in
        myRectangle = QgsRectangle(96, -152, 160, -120)
        self.mComposerMap.setNewExtent(myRectangle)
        myRectangle2 = QgsRectangle(0, -256, 256, 0)
        overviewMap.setNewExtent(myRectangle2)
        overviewMap.overview().setFrameMap(self.mComposerMap.id())
        overviewMap.overview().setInverted(True)
        checker = QgsCompositionChecker('composermap_overview_invert', self.mComposition)
        checker.setControlPathPrefix("composer_mapoverview")
        myTestResult, myMessage = checker.testComposition()
        self.mComposition.removeComposerItem(overviewMap)
        assert myTestResult, myMessage

    def testOverviewMapCenter(self):
        overviewMap = QgsComposerMap(self.mComposition, 20, 130, 70, 70)
        overviewMap.setFrameEnabled(True)
        overviewMap.setLayers([self.raster_layer])
        self.mComposition.addComposerMap(overviewMap)
        # zoom in
        myRectangle = QgsRectangle(192, -288, 320, -224)
        self.mComposerMap.setNewExtent(myRectangle)
        myRectangle2 = QgsRectangle(0, -256, 256, 0)
        overviewMap.setNewExtent(myRectangle2)
        overviewMap.overview().setFrameMap(self.mComposerMap.id())
        overviewMap.overview().setInverted(False)
        overviewMap.overview().setCentered(True)
        checker = QgsCompositionChecker('composermap_overview_center', self.mComposition)
        checker.setControlPathPrefix("composer_mapoverview")
        myTestResult, myMessage = checker.testComposition()
        self.mComposition.removeComposerItem(overviewMap)
        assert myTestResult, myMessage

    def testMapCrs(self):
        # create composition with composer map
        map_settings = QgsMapSettings()
        map_settings.setLayers([self.vector_layer])
        composition = QgsComposition(QgsProject.instance())
        composition.setPaperSize(297, 210)

        # check that new maps inherit project CRS
        QgsProject.instance().setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))
        map = QgsComposerMap(composition, 20, 20, 200, 100)
        map.setFrameEnabled(True)
        rectangle = QgsRectangle(-13838977, 2369660, -8672298, 6250909)
        map.setNewExtent(rectangle)
        map.setLayers([self.vector_layer])
        composition.addComposerMap(map)

        self.assertEqual(map.crs().authid(), 'EPSG:4326')
        self.assertFalse(map.presetCrs().isValid())

        # overwrite CRS
        map.setCrs(QgsCoordinateReferenceSystem('EPSG:3857'))
        self.assertEqual(map.crs().authid(), 'EPSG:3857')
        self.assertEqual(map.presetCrs().authid(), 'EPSG:3857')
        checker = QgsCompositionChecker('composermap_crs3857', composition)
        checker.setControlPathPrefix("composer_map")
        result, message = checker.testComposition()
        self.assertTrue(result, message)

        # overwrite CRS
        map.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))
        self.assertEqual(map.presetCrs().authid(), 'EPSG:4326')
        self.assertEqual(map.crs().authid(), 'EPSG:4326')
        rectangle = QgsRectangle(-124, 17, -78, 52)
        map.zoomToExtent(rectangle)
        checker = QgsCompositionChecker('composermap_crs4326', composition)
        checker.setControlPathPrefix("composer_map")
        result, message = checker.testComposition()
        self.assertTrue(result, message)

        # change back to project CRS
        map.setCrs(QgsCoordinateReferenceSystem())
        self.assertEqual(map.crs().authid(), 'EPSG:4326')
        self.assertFalse(map.presetCrs().isValid())

    # Fails because addItemsFromXml has been commented out in sip
    @unittest.expectedFailure
    def testuniqueId(self):
        doc = QDomDocument()
        documentElement = doc.createElement('ComposerItemClipboard')
        self.mComposition.writeXml(documentElement, doc)
        self.mComposition.addItemsFromXml(documentElement, doc, 0, False)

        # test if both composer maps have different ids
        newMap = QgsComposerMap()
        mapList = self.mComposition.composerMapItems()

        for mapIt in mapList:
            if mapIt != self.mComposerMap:
                newMap = mapIt
                break

        oldId = self.mComposerMap.id()
        newId = newMap.id()

        self.mComposition.removeComposerItem(newMap)
        myMessage = 'old: %s new: %s' % (oldId, newId)
        assert oldId != newId, myMessage

    def testWorldFileGeneration(self):
        myRectangle = QgsRectangle(781662.375, 3339523.125, 793062.375, 3345223.125)
        self.mComposerMap.setNewExtent(myRectangle)
        self.mComposerMap.setMapRotation(30.0)

        self.mComposition.setGenerateWorldFile(True)
        self.mComposition.setReferenceMap(self.mComposerMap)

        p = self.mComposition.computeWorldFileParameters()
        pexpected = (4.180480199790922, 2.4133064516129026, 779443.7612381146,
                     2.4136013686911886, -4.179969388427311, 3342408.5663611)
        ptolerance = (0.001, 0.001, 1, 0.001, 0.001, 1e+03)
        for i in range(0, 6):
            assert abs(p[i] - pexpected[i]) < ptolerance[i]


if __name__ == '__main__':
    unittest.main()
