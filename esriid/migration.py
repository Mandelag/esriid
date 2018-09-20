"""
    Extract properties from layers in MapDocument (.mxd) files.
    Documentation: 
        1. MapDocument http://desktop.arcgis.com/en/arcmap/10.3/analyze/arcpy-mapping/mapdocument-class.htm
        
    @author Keenan Mandela Gebze 
    @ver 3 September 2018
"""

import arcpy.mapping
import etl
import os, sys

def traverse_mxd(root_dir, filter=lambda x: x.endswith("mxd")):
    """ 
        Listing of all .mxd file in a given root directory and their sub-directory.
        Returns the list of path to the.file mxd.
    """
    result = []
    for files in os.walk(root_dir):
        dir = files[0]
        for file in files[2]:
            if filter(file):
                result.append(os.path.join(dir, file))
    return result

def list_mxd_props(mxd, result):
    """
        Extract properties from the .mxd files.
        It is implemented in the etl module.
    """
    doc = arcpy.mapping.MapDocument(mxd)
    doc_properties = (str(doc.filePath), str(doc.title))
    item_count = 0
    for layer in arcpy.mapping.ListLayers(doc):
        item_count += 1
        lp = [x[1] for x in etl.layer_properties_mapping(layer)]
        if lp:
            result( doc_properties + (str(item_count),) + tuple(lp))
    for tv in arcpy.mapping.ListTableViews(doc):
        item_count += 1
        tvp = [x[1] for x in etl.tableview_properties_mapping(tv)]
        if tvp:
            result( doc_properties + (str(item_count),) + tuple(tvp))

def list_mxd_layers(mxd_path, result):
    """
        Listing layers in a mxd.
    """
    mxd = arcpy.mapping.MapDocument(mxd_path)
    for layer in arcpy.mapping.ListLayers(mxd):
        result(mxd, layer)
            
def join_check(lyr):
    """ 
        Check layer that uses join.
        https://gis.stackexchange.com/questions/7703/detecting-join-programmatically-using-arcpy 
    """
    fList = arcpy.Describe(lyr).fields
    for f in fList:
        if f.name.find(lyr.datasetName) > -1:
            return True
    return False