import wget

class MapManager:
    OSM_API_URL = "http://overpass-api.de/api/map?bbox="

    def download_map(self, map_box, osm_file_path):
        #Create download url by adding the box coordinates
        osm_api_url = MapManager.OSM_API_URL + ",".join(map(str, map_box.get_coords()))

        #Get the osm file
        wget.download(url=osm_api_url, out=osm_file_path)