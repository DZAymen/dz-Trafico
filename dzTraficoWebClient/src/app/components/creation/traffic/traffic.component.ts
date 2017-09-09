import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Message, SelectItem, ConfirmationService } from  'primeng/primeng';

import { Depart } from '../../../domain/depart';
import { Arrival } from '../../../domain/arrival';
import { Accident } from '../../../domain/accident';
import { Location } from '../../../domain/location';

import { OsmService } from '../../../shared/osm.service';
import { DepartPointsService } from './depart-point.service';
import { ArrivalPointsService } from './arrival-point.service';
import { AccidentPointsService } from './accident-point.service';

declare var google: any;
@Component({
  moduleId:module.id,
  selector: 'app-traffic',
  templateUrl: './traffic.component.html',
  styleUrls: ['./traffic.component.css'],
  providers: [DepartPointsService, ArrivalPointsService, AccidentPointsService, ConfirmationService]
})
export class TrafficComponent implements OnInit {

  departPoints: Depart[]=[];
  arrivalPoints: Arrival[]=[];
  accidentPoints: Accident[]=[];

  /* Map */
  map:any;
  options: any;
  overlays: any[];
  mapTypeIds:any[]=[];
  infoWindow: any;

  /* Dialog */
  dialogVisible: boolean;
  departDialog: boolean= false; accidentDialog: boolean= false;
  removeMarker: boolean= false;

  selectedType: string;
  markerTypes: SelectItem[];
  position= new Location();

  /* Data  */
  markerName: string;
  selectedPosition: any;
  flow:number; departTime: number;
  accidentTime: number; accidentDuration: number;


    constructor(
          private router: Router,
          private osmService : OsmService,
          private departPointService: DepartPointsService,
          private arrivalPointService : ArrivalPointsService,
          private accidentPointService: AccidentPointsService,
          private confirmationService: ConfirmationService
        ){
              osmService.initMapStyle(google, this.mapTypeIds);
    }

    getAllPoints() {
      this.departPointService.getDepartPoints()
          .then(departs => this.departPoints = []);
      this.arrivalPointService.getArrivalPoints()
          .then(arrivals => this.arrivalPoints = []);
     this.accidentPointService.getAccidentPoints()
         .then(accidents => this.accidentPoints = []);
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

        this.getAllPoints();
    }

    // map toolabar child component
    showDialog(type: string){
      if (type == 'depart'){
          this.departDialog= true;
          this.accidentDialog= false;
      }
      else if (type == 'accident') {
          this.accidentDialog= true;
          this.departDialog= false;
      }else{
        this.departDialog= false;
        this.accidentDialog= false;
      }
    }

    deletePoint(remove : boolean){
      this.removeMarker= remove;
    }

    setMap(event) {
        this.map = event.map;
        this.osmService.getOsmMapType(this.map, google);
    }

    handleMapClick(event){
       this.selectedPosition= event.latLng;
       this.position.setLocation(
           this.selectedPosition.lat(),
           this.selectedPosition.lng()
       )
       this.dialogVisible= true;
    }

    handleOverlayClick(event){
      let obj= event.overlay;
      if (!this.removeMarker){
         let label= event.overlay.getLabel()
         this.infoWindow.setContent(
           '<p> '+label+'</p>');
         this.infoWindow.open(event.map, event.overlay)
         //event.map.setCenter(event.overlay.getPosition());
       }else{
         this.confirmationService.confirm({
               message: 'Voulez vous vraiment supprimer ce point?',
               header: 'Confirmation de supprimeression',
               icon: 'fa fa-trash',
               accept: () => {
                  let marker= event.overlay;
                  let point= JSON.parse(marker.name);
                  if(point._type === 'depart') {
                    this.departPointService.delete(point._id)
                    .then(() => {
                        //this.arrivalPoints= this.arrivalPoints.filter(p => p !== marker.label);
                        this.overlays= this.overlays.filter(p=> p !== marker);
                     })
                  }else if (point.type === 'arrival'){
                    this.arrivalPointService.delete(point._id)
                    .then(() => {
                        //this.arrivalPoints= this.arrivalPoints.filter(p => p !== marker.label);
                        this.overlays= this.overlays.filter(p=> p !== marker);
                     })
                  }else {
                    this.accidentPointService.delete(point._id)
                    .then(() => {
                        //this.arrivalPoints= this.arrivalPoints.filter(p => p !== marker.label);
                        this.overlays = this.overlays.filter(p=> p !== marker);
                     })
                  }
               }
           });
       }
    }

    addPoint() {
      if (this.departDialog) {
        let depart= new Depart( this.position, this.departTime, this.flow);
        this.departPointService.create(depart)
          .then(dept => {
            console.log(dept);
            this.departPoints.push(dept);
            this.drawMarker(dept,'depart');
          });
      }else if (this.accidentDialog){
        let accident= new Accident(this.position, this.accidentTime, this.accidentDuration);
        this.accidentPointService.create(accident)
          .then(acc => {
            this.accidentPoints.push(acc);
            this.drawMarker(acc,'accident');
        });
      }else{
        let arrival= new Arrival(this.position);
        this.arrivalPointService.create(arrival)
          .then(arr => {
            this.arrivalPoints.push(arr);
            this.drawMarker(arr, 'arrival');
        });
      }
    }

    // addPoint() {
    //   if (this.departDialog) {
    //     let depart= new Depart( this.position, this.departTime, this.flow);
    //     this.departPointService.create(depart);
    //     this.departPoints.push(depart);
    //     this.drawMarker(depart,'depart');
    //   }else if (this.accidentDialog){
    //     let accident= new Accident(this.position, this.accidentTime, this.accidentDuration);
    //     this.accidentPointService.create(accident);
    //     this.accidentPoints.push(accident);
    //     this.drawMarker(accident,'accident');
    //   }else{
    //     let arrival= new Arrival(this.position);
    //     this.arrivalPointService.create(arrival);
    //     this.arrivalPoints.push(arrival);
    //     this.drawMarker(arrival, 'arrival');
    //   }
    // }

    drawMarker(obj: any,type: string){
      console.log(obj)
      this.overlays.push(new google.maps.Marker({
          position: {lat: this.selectedPosition.lat(), lng: this.selectedPosition.lng()},
          name: JSON.stringify({ _id: obj.id , _type: type}), // save the obj.id into marker.label to facilitate the suppression of the point
          label: this.markerName,
          draggable: true,
          icon:`../../../assets/images/typeMarker/${type}.ico`
        }));
       this.markerName= null;
       this.dialogVisible= false;
     }

     prev(){
       this.router.navigate(['/map']);
     }

     next(){
       this.router.navigate(['/vehicle']);
     }
}
