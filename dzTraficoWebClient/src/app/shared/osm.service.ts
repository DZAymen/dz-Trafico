import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import { Zone } from '../domain/zone';




@Injectable()
export class OsmService {

  private mapURL= "http://127.0.0.1:8000/api/creation/map";
  private headers = new Headers({'Content-Type': 'application/json'});


  constructor(private http: Http) {}


  initMapStyle(google: any, mapTypeIds: any[]){
        // define map's type to be displayed
        for (var type in google.maps.MapTypeId) {
            mapTypeIds.push(google.maps.MapTypeId[type]);
        }
            mapTypeIds.push("OSM");
  }

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

        this.http.post(this.mapURL, JSON.stringify({
            left: southWest.lng(),
            bottom: southWest.lat(),
            right: northEast.lng(),
            top: northEast.lat()
         }), {headers: this.headers})
        .toPromise().catch(this.handleError);

  }

  getBounds(): Promise<Zone> {
     return this.http.get(this.mapURL)
                .toPromise()
                .then(response => response.json() as Zone)
                .catch(this.handleError);
  }

  private handleError(error : any){
    console.error('Erreur ', error);
    return Promise.reject(error.message || error);
  }


}
