"""
    Extracted columns (column header)--arcpy object properties mapping.
    Examples of arcpy object: MapDocument, SpatialReference, Layer, FeatureClass, etc..
    
    @author Keenan Mandela Gebze
    @ver 29 August 2018
"""
import esriid

DEFAULT_CLASSIFIER_CACHER = esriid.DatasetClassifier()

def tableview_properties_mapping(tv):
    """ An example of extract table implementation """
    properties = []
    try:
        properties = [
            ("Type", "TableView"),
            ("Name", tv.name),
            ("Long name", ""),
            ("Layer type", "Table"),
            ("Definition query", tv.definitionQuery),
            ("Is broken", "Broken" if tv.isBroken else ""),
            #("Workspace path", tv.workspacePath),
            ("Dataset name", tv.datasetName),
            ("Datasource", tv.dataSource)
        ]
        serviceProps = [
            ("Service type", ""),
            ("Server", ""),
            ("Service", ""),
            ("Database", ""),
            ("Username", ""),
            ("Authentication mode", ""),
            ("Version", "")
        ]
        properties + serviceProps
    except ValueError: # handle TableView.dataSource read from previous version of .mxd .. 10.3 ..?
        properties = ["Value error", ("", ""), ("", ""), ("", "") ,("" ,""), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", "") ,("" ,""), ("", ""), ("", ""), ("", ""), ("", "")]
    return properties

def layer_properties_mapping(layer, cacher=DEFAULT_CLASSIFIER_CACHER):
    """ An example of extract layer implementation """
    #if layer.isGroupLayer:
    #    return None
    properties = [
        ("Type", "Layer"),
        ("Name", layer.name),
        ("Long Name", layer.longName),
        ("Layer Type", "BasemapLayer" if layer.isBasemapLayer else 
          "FeatureLayer" if layer.isFeatureLayer else 
            "NetworkAnalystLayer" if layer.isNetworkAnalystLayer else 
              "RasterizingLayer" if layer.isRasterizingLayer else
                "RasterLayer" if layer.isRasterLayer else
                  "ServiceLayer" if layer.isServiceLayer else ""),
        ("Definition query", "" if not layer.supports("DEFINITIONQUERY") else layer.definitionQuery),
        ("Is broken", "Broken" if layer.isBroken else ""),
        #("Workspace path", "" if layer.supports("WORKSPACEPATH") else layer.workspacePath),
        ("Dataset name", "" if not layer.supports("DATASETNAME") else layer.datasetName),
        ("Datasource", "" if not layer.supports("DATASOURCE") else layer.dataSource),
        ("Datasource type", cacher.classify_dataset(layer.dataSource))
    ]
    
    serviceProps = [("Service type", "" if not layer.supports("SERVICEPROPERTIES") else layer.serviceProperties.get("ServiceType", "")),
        ("Server", "" if not layer.supports("SERVICEPROPERTIES") else layer.serviceProperties.get("Server", "")),
        ("Service", "" if not layer.supports("SERVICEPROPERTIES") else layer.serviceProperties.get("Service", "")),
        ("Database", "" if not layer.supports("SERVICEPROPERTIES") else layer.serviceProperties.get("Database", "")),
        ("Username", "" if not layer.supports("SERVICEPROPERTIES") else layer.serviceProperties.get("UserName", "")),
        ("Authentication mode", "" if not layer.supports("SERVICEPROPERTIES") else layer.serviceProperties.get("AuthenticationMode", "")),
        ("Version", "" if not layer.supports("SERVICEPROPERTIES") else layer.serviceProperties.get("Version", ""))
    ]
    properties + serviceProps
    return properties