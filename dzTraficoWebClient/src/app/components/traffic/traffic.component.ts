import { Component, OnInit } from '@angular/core';
import { Message, SelectItem } from  'primeng/primeng';

import { MARKER_TYPES } from './markertype.config';

import { Depart } from '../../domain/depart';
import { DepartPointsService } from './depart-point.service';


declare var google: any;
@Component({
  moduleId:module.id,
  selector: 'app-traffic',
  templateUrl: './traffic.component.html',
  styleUrls: ['./traffic.component.css'],
  providers: [DepartPointsService]
})
export class TrafficComponent implements OnInit {

  departPoints: Depart[];

  /* Map */
  options: any;
  overlays: any[];
  infoWindow: any;

  /* Dialog  */
  dialogVisible: boolean;
  markerName: string;
  selectedPosition: any;
  selectedType: string;
  markerTypes: SelectItem[];

  /* Data Table */
  debit : number;
  msgs: Message[]=[];

    constructor(private departPointService: DepartPointsService){
    }

    getDeparts() {
      this.departPointService
          .getDepartPoints()
          .then(departs => this.departPoints = departs);
    }

    addDepart(name: string) {
    //  let depart = new Depart();
      name = name.trim();
      if (!name) { return; }
      this.departPointService.create(name)
        .then(depart => {
          this.departPoints.push(depart);
          this.drawMarker();
        });
    }

    // deleteDepart(depart: Depart): void {
    //   this.departPointService
    //       .delete(depart.id)
    //       .then(() => {
    //         this.departPoints = this.departPoints.filter(h => h !== depart);
    //       });
    // }

    ngOnInit() {
        this.options = {
                    center: {lat: 36.7596737, lng: 3.1365537},
                    zoom: 12,
                    streetViewControl: false
                };
        this.overlays = [] ;
        this.infoWindow = new google.maps.InfoWindow();

        this.markerTypes = MARKER_TYPES;

        this.getDeparts();
    }

    handleMapClick(event){
      this.dialogVisible= true;
      this.selectedPosition= event.latLng;
    }

    handleOverlayClick(event){
      if (event.overlay.getTitle != undefined){
         let title= event.overlay.getTitle()
         this.infoWindow.setContent(' '+ title+ ' ');
         this.infoWindow.open(event.map, event.overlay)
         event.map.setCenter(event.overlay.getPosition());
       }
    }

    drawMarker(){
      this.overlays.push(new google.maps.Marker({
          position: { lat: this.selectedPosition.lat(), lng: this.selectedPosition.lng()},
          title: this.markerName,
          draggable: true,
          icon:"../../../assets/images/typeMarker/arrival.ico"
        }));
       this.markerName= null;
       this.dialogVisible= false;
       this.msgs.push({severity:'success', summary:'test', detail: ''});
     }

}
