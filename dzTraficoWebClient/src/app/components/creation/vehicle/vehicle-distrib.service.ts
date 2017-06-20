import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { VehicleDistribution} from '../../../domain/vehicle-distrib';

@Injectable()
export class VehicleDistribService {

  private apiURL = 'api/vehpourcentage';
  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) { }

  vDistriConfig(VehicleDistrib: VehicleDistribution[]): Promise<VehicleDistribution>{
     return this.http
                .post(this.apiURL, VehicleDistrib, {headers: this.headers})
                .toPromise()
                .then(res => res.json().data as VehicleDistribution)
                .catch(this.handleError);
  }

  private handleError(error : any){
    console.error('Erreur ', error);
    return Promise.reject(error.message || error);
  }

}
