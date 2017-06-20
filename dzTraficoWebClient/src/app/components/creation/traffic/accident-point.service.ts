import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Accident } from '../../../domain/accident';

@Injectable()
export class AccidentPointsService {

  private apiURL = 'api/accidents';
  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) { }

  getAccidentPoints(): Promise<Accident[]> {
     return this.http.get(this.apiURL)
                .toPromise()
                .then(response => response.json().data as Accident[])
                .catch(this.handleError);
  }

  getAccidentPointById(id: number): Promise<Accident>{
     return this.http.get(`${this.apiURL}/${id}`)
               .toPromise()
               .then(response => response.json().data as Accident)
               .catch(this.handleError);
  }

  delete(id: number): Promise<void>{
     return this.http.delete(`${this.apiURL}/${id}`, {headers: this.headers})
                .toPromise()
                .then(() => null)
                .catch(this.handleError);
  }

  create(accident: Accident): Promise<Accident>{
     return this.http
                .post(this.apiURL, accident, {headers: this.headers})
                .toPromise()
                .then(res => res.json().data as Accident)
                .catch(this.handleError);

  }

  update(Accident: Accident): Promise<Accident>{
    return this.http
               .put(this.apiURL, JSON.stringify({Accident: Accident}), {headers: this.headers})
               .toPromise()
               .then(() => Accident)
               .catch(this.handleError);
  }

  private handleError(error : any){
    console.error('Erreur ', error);
    return Promise.reject(error.message || error);
  }

}
