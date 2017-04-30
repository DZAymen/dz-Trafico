import os
import osmapi
from dicttoxml import dicttoxml
from datetime import datetime

class MapManager:
    __osmApi = osmapi.OsmApi()

    def download_map(self, map_box):
        directory_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        directory_path = os.path.join(os.path.normpath(os.getcwd()), "dzTrafico\\SimulationFiles")
        directory_path = os.path.join(directory_path, directory_name)
        os.makedirs(directory_path)
        map_data = MapManager.__osmApi.Map(map_box.left, map_box.bottom, map_box.right, map_box.top)
        xml_file = dicttoxml(map_data)
        file = open(directory_path + "\\map.net.xml", "wb")
        file.write(xml_file)
        file.close()
        return directory_path + "\\map.net.xml"