import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Arrival } from '../../../domain/arrival';

@Injectable()
export class ArrivalPointsService {

  //private apiURL = "http://127.0.0.1:8000/api/creation/trafficflow/arrivals";
  private apiURL = "api/arrivals";
  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) { }

  getArrivalPoints(): Promise<Arrival[]> {
     return this.http.get(this.apiURL)
                .toPromise()
                .then(response => response.json().data as Arrival[])
                .catch(this.handleError);
  }

  getArrivalPointById(id: number): Promise<Arrival>{
     return this.http.get(`${this.apiURL}/${id}`)
               .toPromise()
               .then(response => response.json().data as Arrival)
               .catch(this.handleError);
  }

  delete(id: number): Promise<void>{
     return this.http.delete(`${this.apiURL}/${id}`, {headers: this.headers})
                .toPromise()
                .then(() => null)
                .catch(this.handleError);
  }

  create(arrival: Arrival): Promise<Arrival>{
     return this.http
                .post(this.apiURL, arrival, {headers: this.headers})
                .toPromise()
                .then(res => res.json().data as Arrival)
                .catch(this.handleError);

  }

  update(Arrival: Arrival): Promise<Arrival>{
    return this.http
               .put(this.apiURL, JSON.stringify({Arrival: Arrival}), {headers: this.headers})
               .toPromise()
               .then(() => Arrival)
               .catch(this.handleError);
  }

  private handleError(error : any){
    console.error('Erreur ', error);
    return Promise.reject(error.message || error);
  }

}
