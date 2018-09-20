"""
    Collection of utility scripts to make 
    GIS Engineer life's easier.
    
    @author Keenan Mandela Gebze
    @ver 20 September 2018
"""

def hello():
    print("Hello from Esri Indonesia!")

class DatasetClassifier:
    """
        Return dataset classifier that has a cache enabled.
        Cache is used because arcpy.Exists and arcpy.Describe
        is relatively expensive process.
    """
    def __init__(this):
        reset_cache(this)
    
    def classify_dataset(this, path_to_dataset):
        """
            Given a path to a dataset ds, return the dataset type.
            @param path_to_dataset path to target dataset
            @return the dataType of the dataset in the given path. 
                Return not_exists if dataset is not found.
        """
        type = this.cache.get(path_to_dataset, "")
        if type == "":
            if arcpy.Exists(path_to_dataset):
                type = arcpy.Describe(path_to_dataset).dataType
            else:
                type = "not_exists"
            cache[path_to_dataset] = type
        else:
            #print("using cache!")
            pass
        return type
        
    def reset_cache(this):
        """
            Reset the cache.
        """
        this.cache = {}
    