import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { VehicleType } from '../../domain/vehicle-type';

@Injectable()
export class VehicleService {

//  private apiURL = 'http://localhost:8000/api/?format=json';


  constructor(private http: Http) {}

  getVehicleType(){
      return this.http.request('./../../assets/vehicle-type.json')
          .map(res => <VehicleType[]> res.json());

            // .toPromise()
            // .then(res => <VehicleType[]> res.json())
            // .then(data => { return data; });

  }

}
