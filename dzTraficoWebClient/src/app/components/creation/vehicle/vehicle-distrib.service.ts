import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { VehicleDistribution} from '../../../domain/vehicle-distrib';

export interface vehDistriI {
  id: number,
  percentage: number
}

@Injectable()
export class VehicleDistribService {

  private apiURL = "http://127.0.0.1:8000/api/creation/vehicletypespercentages";
  //private apiURL= "api/vehpourcentage"
  private headers = new Headers({'Content-Type': 'application/json'});
  private vehDistriToSend: vehDistriI[]=[];



  constructor(private http: Http) { }

  vDistriConfig(VehicleDistrib: VehicleDistribution[]){
    let vd;
    for (let item of VehicleDistrib) {
       vd = {
         id: item.vehicleType.id,
         percentage: item.percentage
      }
       this.vehDistriToSend.push(vd);
    }
    console.log( this.vehDistriToSend);
     return this.http
                .post(this.apiURL, this.vehDistriToSend, {headers: this.headers})
                .toPromise()
                .then(res => res.json() as vehDistriI)
                .catch(this.handleError);
  }

  private handleError(error : any){
    console.error('Erreur ', error);
    return Promise.reject(error.message || error);
  }

}
