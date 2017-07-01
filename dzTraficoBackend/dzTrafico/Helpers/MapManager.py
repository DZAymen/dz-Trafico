import os
from datetime import datetime
import wget

class MapManager:
    OSM_API_URL = "http://overpass-api.de/api/map?bbox="

    def download_map(self, map_box):
        #Create the directory for the new simulation
        directory_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        directory_path = os.path.join(os.path.normpath(os.getcwd()), "dzTrafico\\SimulationFiles")
        directory_path = os.path.join(directory_path, directory_name)
        os.makedirs(directory_path)
        self.osm_file_path = directory_path + "\\map_bbox.osm.xml"

        #Create download url by adding the box coordinates
        osm_api_url = MapManager.OSM_API_URL + ",".join(map(str, map_box.get_coords()))

        #Get the osm file
        wget.download(url=osm_api_url, out=self.osm_file_path)

        return self.osm_file_path