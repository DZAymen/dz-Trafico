import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { VehicleType } from '../../../domain/vehicle-type';

@Injectable()
export class VehicleTypeService {

  //private apiURL = "http://127.0.0.1:8000/api/creation/vehicletypes";
  private apiURL= "api/vehicleTypes"
  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) { }

  getVehicleTypes(): Promise<VehicleType[]> {
     return this.http.get(this.apiURL)
                .toPromise()
                .then(response => response.json().data as VehicleType[])
                .catch(this.handleError);
  }

  getVehicleTypeById(id: number): Promise<VehicleType>{
     return this.http.get(`${this.apiURL}/${id}`)
               .toPromise()
               .then(response => response.json().data as VehicleType)
               .catch(this.handleError);
  }

  delete(id: number): Promise<void>{
     return this.http.delete(`${this.apiURL}/${id}`, {headers: this.headers})
                .toPromise()
                .then(() => null)
                .catch(this.handleError);
  }

  create(vType: VehicleType): Promise<VehicleType>{
     return this.http
                .post(this.apiURL, vType ,{headers: this.headers})
                .toPromise()
                .then(res => res.json().data as VehicleType)
                .catch(this.handleError);

  }

  update(VehicleType: VehicleType): Promise<VehicleType>{
    return this.http
               .put(this.apiURL, JSON.stringify({VehicleType: VehicleType}), {headers: this.headers})
               .toPromise()
               .then(() => VehicleType)
               .catch(this.handleError);
  }

  private handleError(error : any){
    console.error('Erreur ', error);
    return Promise.reject(error.message || error);
  }

}
