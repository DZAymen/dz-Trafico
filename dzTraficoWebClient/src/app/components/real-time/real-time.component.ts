import { Component, OnInit } from '@angular/core';

import { WebsocketService } from './websocket.service';
import {RealTimeService} from './real-time.service';
import { OsmService } from '../../shared/osm.service';

import {Message} from 'primeng/primeng';

import {Lc} from '../../domain/lc';
import {Vsl} from '../../domain/vsl';
import {TraficState} from '../../domain/trafic-state';

declare var google: any;
@Component({
  selector: 'app-real-time',
  templateUrl: './real-time.component.html',
  styleUrls: ['./real-time.component.css'],
  providers: [WebsocketService, RealTimeService, OsmService]
})
export class RealTimeComponent implements OnInit {

  lcList: Lc[]=[];
  vslList: Vsl[]=[];
  traficStateList: TraficState[]=[];

  map: any;
  options: any;
  overlays: any[];
  mapTypeIds:any[]=[];
  infoWindow: any;
  msgs: Message[] = [];

  constructor(
    private realTimeService: RealTimeService,
    private osmService : OsmService,
    ){
		// realTimeService.recommandations.subscribe(rec => {
    //   console.log("recommandations from websocket: " + rec);
		// });
	}


  ngOnInit() {
    this.realTimeService.getTraficState().then(traficState => this.drawPolyline(traficState));
    this.realTimeService.getRecommandation().then(laneChange => this.lcList = laneChange);
    this.realTimeService.getVsl().then(variableSpeedLimit => this.vslList = variableSpeedLimit);

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

  }

  // When map is ready then define variable map
  setMap(event) {
      this.map = event.map;
      this.osmService.getOsmMapType(this.map, google);

  }

  handleOverlayClick(event){
    this.msgs.push({severity: event.overlay.severity,
                    summary:'Segment',
                    detail: 'Densité: ' + event.overlay.density +' Vitesse: ' + event.overlay.current_speed
                   });
  }

 lancerSumo(){
   this.realTimeService.startSimulation();
 }

  drawPolyline( stListe: TraficState[]){
    let polyColor: string;
    let severity: string;
    for (let ts of stListe) {

      // couleur du polyline
      if (ts.current_speed <= 40){ polyColor= '#FF0000'; /* rouge */ severity= 'error'
    }else if (ts.current_speed > 40 && ts.current_speed <= 70 ) { polyColor= '#FF4500'; /* orange */ severity= 'warn'
  }else {  polyColor= '#9ACD32'; /* vert */ severity= 'success'}

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
