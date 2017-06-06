import { Component, OnInit } from '@angular/core';
import { VehicleService } from './vehicle.service';
import { VehicleType } from '../../domain/vehicle-type';


@Component({
  selector: 'app-vehicle',
  templateUrl: './vehicle.component.html',
  styleUrls: ['./vehicle.component.css'],
  providers: [VehicleService]
})
export class VehicleComponent implements OnInit {

  dialogVisible: boolean= false;
  pourcentage: number= 30;

  vehicleTypes: any[];
  cols: any[];

  // dialog field
  accel :number;
  decel: number;
  impatience: number;

  constructor(private vehicleService: VehicleService ) { }

  ngOnInit() {

    this.vehicleService.getVehicleType()
          .subscribe( res => this.vehicleTypes= res);
    this.cols = [
           {field: 'id', header: 'Model'},
           {field: 'accel', header: 'Accel'},
           {field: 'decel', header: 'Decel'},
           {field: 'impatience', header: 'Impatience'}
       ];
  }

  showDialog(){
    this.dialogVisible= true;
  }

  addVehicleType(){
  var newType = {
   id : 5,
   accel: this.accel,
   decel: this.decel,
   impatience: this.impatience
 }
  this.vehicleTypes.push(newType);
  }
}
