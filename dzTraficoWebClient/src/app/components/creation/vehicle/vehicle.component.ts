import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { DATATABLE_FIELD } from './table-field.config';
import { VehicleTypeService } from './vehicle.service';
import { VehicleDistribService } from './vehicle-distrib.service';

import { VehicleDistribution } from '../../../domain/vehicle-distrib';
import { VehicleType } from '../../../domain/vehicle-type';


@Component({
  selector: 'app-vehicle',
  templateUrl: './vehicle.component.html',
  styleUrls: ['./vehicle.component.css'],
  providers: [VehicleTypeService, VehicleDistribService]
})
export class VehicleComponent implements OnInit {

  dialogVisible: boolean= false;

  vehiclesDistri: VehicleDistribution[]=[];
  cols: any[];

  // dialog field
  newType= new VehicleType();

  constructor(
    private router: Router,
    private vehicleTypeService: VehicleTypeService,
    private vehicleDistribService: VehicleDistribService
    ) { }

  ngOnInit() {

    this.cols = DATATABLE_FIELD.filter(colomns => colomns);
  }

  showDialog(){
    this.dialogVisible= true;
  }

  addVehicleType(){
      this.vehicleTypeService.create(this.newType).then(
        vehtype => {
          let newVDistri = new VehicleDistribution(vehtype);
          this.vehiclesDistri.push(newVDistri);
          console.log(this.vehiclesDistri);
        }
      )
      this.dialogVisible = false;
      //this.newType= null;
  }

  prev(){
    this.router.navigate(['/trafficflow']);
  }

  next(){
    this.vehicleDistribService.vDistriConfig(this.vehiclesDistri)
        .then( vDistri => console.log(vDistri));
    this.router.navigate(['/start']);
  }

  /*private transformToDist(vTypes: VehicleType[]){
      for (let vt of vTypes) {
        this.vehiclesDistri.push(new VehicleDistribution(vt));
      }
  }*/
}
