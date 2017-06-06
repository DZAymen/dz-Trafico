import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

@Injectable()
export class OsmService {

  constructor(private http: Http) {}

  // To display the osm map
  getOsmMapType (map: any, google: any){
      map.mapTypes.set("OSM", new google.maps.ImageMapType({
          getTileUrl: function(coord, zoom) {
            return ("http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png");
          },
          tileSize: new google.maps.Size(256, 256),
          name: "Open Street Map",
          maxZoom: 18
      }));
  }

 // Call the backend to build .osm file
  buildOsmFile(northEast: any, southWest: any){

  }

}
