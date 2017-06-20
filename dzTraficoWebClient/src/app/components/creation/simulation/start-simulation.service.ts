import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { SimulationConfig } from '../../../domain/simul-config';

@Injectable()
export class StartSimulationService {

  private apiURL = 'api/sensors';
  private headers = new Headers({'Content-Type': 'application/json'});

  constructor(private http: Http) { }

  simulationConfig(config: SimulationConfig): Promise<SimulationConfig>{
     return this.http
                .post(this.apiURL, config, {headers: this.headers})
                .toPromise()
                .then(res => res.json().data as SimulationConfig)
                .catch(this.handleError);
  }

  private handleError(error : any){
    console.error('Erreur ', error);
    return Promise.reject(error.message || error);
  }

}
