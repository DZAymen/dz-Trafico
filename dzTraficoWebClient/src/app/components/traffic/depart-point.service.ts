import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Depart } from '../../domain/depart';

@Injectable()
export class DepartPointsService {

  private apiURL = 'api/departs'; 
  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) { }

  getDepartPoints(): Promise<Depart[]> {
     return this.http.get(this.apiURL)
                .toPromise()
                .then(response => response.json().data as Depart[])
                .catch(this.handleError);
  }

  getDepartPointById(id: number): Promise<Depart>{
    return this.http.get(`${this.apiURL}/${id}`)
               .toPromise()
               .then(response => response.json().data as Depart)
               .catch(this.handleError);
  }

  delete(id: number): Promise<void>{
     return this.http.delete(`${this.apiURL}/${id}`, {headers: this.headers})
                .toPromise()
                .then(() => null)
                .catch(this.handleError);
  }

  create(depart: Depart): Promise<Depart>{
     return this.http
                .post(this.apiURL, JSON.stringify({depart: Depart}), {headers: this.headers})
                .toPromise()
                .then(res => res.json().data as Depart)
                .catch(this.handleError);

  }

  update(depart: Depart): Promise<Depart>{
    return this.http
               .put(this.apiURL, JSON.stringify({depart: Depart}), {headers: this.headers})
               .toPromise()
               .then(() => depart)
               .catch(this.handleError);
  }

  private handleError(error : any){
    console.error('Erreur ', error);
    return Promise.reject(error.message || error);
  }






}
