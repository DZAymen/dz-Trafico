import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import 'rxjs/add/operator/map';
import 'rxjs/add/operator/mergeMap';

@Injectable()
export class GeocodingService {

  private geocodeURL     = "http://maps.googleapis.com/maps/api/geocode/json?address=";
  private ipFinderURL    = "http://ipv4.myexternalip.com/json";
  private ipToAdresseURL = "http://freegeoip.net/json/";

  constructor(private http:Http) { }

  geocode(address: string) {
        return this.http
            .get( this.geocodeURL + encodeURIComponent(address))
            .map(res => res.json())
            .map(result => {
                if (result.status !== "OK") { throw new Error("unable to geocode address"); }
                  return result.results[0].geometry.location;
            });
    }


    getCurrentLocation() {
         return this.http
          .get(this.ipFinderURL)
          .map(res => res.json().ip)
          .flatMap(ip => this.http.get(this.ipToAdresseURL + ip)) // add later condition when it returns nothing
          .map(res => res.json());
    }

}
