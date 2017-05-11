import os
import osmapi
from dicttoxml import dicttoxml
from datetime import datetime
from dzTrafico.BusinessEntities.MapBox import MapBox
import osmGet

class MapManager:
    __osmApi = osmapi.OsmApi()

    def download_map(self, map_box):
        #Create the directory for the new simulation
        directory_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        directory_path = os.path.join(os.path.normpath(os.getcwd()), "dzTrafico\\SimulationFiles")
        directory_path = os.path.join(directory_path, directory_name)
        os.makedirs(directory_path)
        self.osm_file_path = directory_path + "\\map"

        #Get the osm file
        osmGet.get(["-b", ",".join(map(str, map_box.get_coords())), "-p", self.osm_file_path])

        return self.osm_file_path