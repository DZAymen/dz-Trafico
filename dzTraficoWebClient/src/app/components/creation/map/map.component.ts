import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Message } from  'primeng/primeng';


import { OsmService } from '../../../shared/osm.service';
import { GeocodingService } from './geocoding.service';

declare var google: any;

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css'],
  providers: [GeocodingService]
})
export class MapComponent implements OnInit {

  map: any;
  mapCenter: any;
  address: string="";

  options: any;
  overlays: any[];
  rectangle: any;
  mapTypeIds:any[]=[];
  msgs: Message[]=[];

    constructor(
         private router: Router,
         private osmService: OsmService,
         private geocodingService: GeocodingService){
                 osmService.initMapStyle(google, this.mapTypeIds);
    }

    ngOnInit() {
        this.options = {
                    center: {lat: 36.7596737, lng: 3.1365537},
                    zoom: 12,
                    mapTypeControlOptions: {
                      mapTypeIds: this.mapTypeIds,
                      position: google.maps.ControlPosition.TOP_RIGHT
                      },
                    streetViewControl: false,
                    fullscreenControl: true
                };

        this.overlays = [] ;
    }

    // When map is ready then define variable map
    setMap(event) {
        this.map = event.map;
        this.osmService.getOsmMapType(this.map, google);

        // Center the map on the current location of the user
        // this.geocodingService
        //     .getCurrentLocation()
        //     .subscribe(location => this.map.setCenter(new google.maps.LatLng(
        //      location.latitude, location.longitude
        // )));
    }

    //
    goto() {
       if (this.address) {

       this.geocodingService.geocode(this.address)
       .subscribe(location => {
         this.map.setCenter(new google.maps.LatLng(location.lat , location.lng));
         if (this.map.getZoom() < 14)
            this.map.setZoom(14);
       });

     }
    }

    zoneSelector() {
      if (!this.rectangle){
        this.mapCenter= this.map.getCenter();
        var scale = Math.pow(2,this.map.getZoom());

        this.rectangle = new google.maps.Rectangle({
            editable: true,
            draggable: true,
            strokeColor: '#999999', strokeOpacity: 0.8, strokeWeight: 2,
            fillColor: '#999999', fillOpacity: 0.4,
            bounds: {
              north: this.mapCenter.lat()+ 50 /scale,
              south: this.mapCenter.lat()- 50 /scale,
              east:  this.mapCenter.lng()+ 100/scale,
              west:  this.mapCenter.lng()- 100/scale
          }
        });
        this.overlays.push(this.rectangle);
      }
    }

    networkExport(){
      if (this.rectangle) {
        this.osmService.buildOsmFile(
                this.rectangle.getBounds().getNorthEast(),
                this.rectangle.getBounds().getSouthWest()
        );

      // if l'export à partir du service a réussie
      this.msgs.push({severity:'success', summary:'Export réussi', detail: 'La zone routière a bien été exporté'});
      }
      else {
        this.msgs = [];
        this.msgs.push({severity:'warn', summary:'Aucune zone à exporter', detail: 'Vous devez d\'abord seléctionner une zone'});
      }
    //  this.router.navigate(['/trafficflow']);
    }


}
