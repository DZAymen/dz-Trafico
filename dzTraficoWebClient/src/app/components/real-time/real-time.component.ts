import { Component, OnInit } from '@angular/core';

import { WebsocketService } from './websocket.service';
import {RealTimeService} from './real-time.service';
import { VslService } from './vsl.service';

import { OsmService } from '../../shared/osm.service';


import {Message} from 'primeng/primeng';

import {Lc} from '../../domain/lc';
import {Vsl} from '../../domain/vsl';
import {TraficState} from '../../domain/trafic-state';
import {RealtimeData} from '../../domain/realtime-data';

declare var google: any;
@Component({
  selector: 'app-real-time',
  templateUrl: './real-time.component.html',
  styleUrls: ['./real-time.component.css'],
  providers: [WebsocketService, RealTimeService, VslService, OsmService]
})
export class RealTimeComponent implements OnInit {

  realtimeDataList: RealtimeData;
  lcList: Lc[]=[];
  vslList: Vsl[]=[];
  traficStateList: TraficState[]=[];

  map: any;
  options: any;
  overlays: any[];
  mapTypeIds:any[]=[];
  infoWindow: any;
  rectangle: any;
  msgs: Message[] = [];

  private message = {
    startSim: true
  }

  constructor(
    private realTimeService: RealTimeService,
    private osmService : OsmService,
    private wsService: WebsocketService,
    private vslService: VslService
    ){
       this.osmService.initMapStyle(google, this.mapTypeIds);
       this.realTimeService.connectToRealTime(this.wsService);

       this.realTimeService.startSimulationMsg.subscribe( rt => {
        console.log("VSL from websocket: ", rt);
         this.realtimeDataList = rt;
         this.lcList= this.realtimeDataList.lc;
         this.vslList= this.realtimeDataList.vsl;
        this.drawPolyline(this.realtimeDataList.trafficState)
  		});
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
    this.infoWindow = new google.maps.InfoWindow();
    this.zoneDelimiter();

  }

  zoneDelimiter() {
     // service pr récupérer bounds
      this.osmService.getBounds().then( zone => {

      this.overlays.push(new google.maps.Polyline({
        path: [
                {lat: zone.top, lng: zone.left},
                {lat: zone.bottom, lng: zone.left}
              ],
        geodesic: true,
        strokeColor: '#999999', strokeOpacity: 0.5, strokeWeight: 2,
      }));

      this.overlays.push(new google.maps.Polyline({
        path: [
                {lat: zone.bottom, lng: zone.left},
                {lat: zone.bottom, lng: zone.right}
              ],
        geodesic: true,
        strokeColor: '#999999', strokeOpacity: 0.5, strokeWeight: 2,
      }));

      this.overlays.push(new google.maps.Polyline({
        path: [
                {lat: zone.bottom, lng: zone.right} ,
                {lat: zone.top, lng: zone.right}
              ],
        geodesic: true,
        strokeColor: '#999999', strokeOpacity: 0.5, strokeWeight: 2,
      }));

      this.overlays.push(new google.maps.Polyline({
        path: [
                {lat: zone.top, lng: zone.right},
                {lat: zone.top, lng: zone.left}
              ],
        geodesic: true,
        strokeColor: '#999999', strokeOpacity: 0.5, strokeWeight: 2,
      }));

     })
 }

  // When map is ready then define variable map
  setMap(event) {
      this.map = event.map;
      this.osmService.getOsmMapType(this.map, google);
  }

  // When map is ready then define variable map
  handleOverlayClick(event){
    this.msgs.push({severity: event.overlay.severity,
                    summary:'Segment',
                    detail: 'Densité: ' + event.overlay.density +' Vitesse: ' + event.overlay.current_speed
                   });
  }


  drawPolyline( stListe: TraficState[]){

    this.overlays = [] ;
    this.zoneDelimiter();

    let polyColor: string;
    let severity: string;
    for (let ts of stListe) {

      // couleur du polyline
     if (ts.current_speed <= 40 && ts.current_speed >= 0){ polyColor= '#FF0000'; /* rouge */ severity= 'error'
   }else if (ts.current_speed > 40 && ts.current_speed <= 60 ) { polyColor= '#FF4500'; /* orange */ severity= 'warn'
   }else if (ts.current_speed > 60 )  {  polyColor= '#9ACD32'; /* vert */ severity= 'success'}

      this.overlays.push(new google.maps.Polyline({
        path: [
                {lat: ts.edge_coords.start.lat, lng: ts.edge_coords.start.lng},
                {lat: ts.edge_coords.end.lat, lng: ts.edge_coords.end.lng}
              ],
        geodesic: true,
        strokeColor: polyColor,
        strokeOpacity: 0.5,
        strokeWeight: 2,
        density: ts.density,
        current_speed: ts.current_speed,
        edge_id: ts.edge_id,
        severity: severity
      }))
    }

  }

}
