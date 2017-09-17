import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { GraphData } from '../../domain/graph-data';
import { Result } from '../../domain/result';

@Injectable()
export class StatService {

  private flowURL = 'http://127.0.0.1:8000/api/statistics/incidentflowstats';
  private densityURL = 'http://127.0.0.1:8000/api/statistics/incidentdensitystats';
  private resultURL = 'http://127.0.0.1:8000/api/statistics/gpm';

  constructor(private http: Http) { }

  getVariations(): Promise<Result[]>{
    return  this.http.get(this.resultURL)
               .toPromise()
               .then(response => response.json() as Result[])
               .catch(this.handleError);
  }

  getFlowDiagramData(): Promise<GraphData>{
      return this.http.get(this.flowURL)
               .toPromise()
               .then(response => response.json() as GraphData)
               .catch(this.handleError);
  }
  getDensityDiagramData(): Promise<GraphData>{
      return this.http.get(this.densityURL)
               .toPromise()
               .then(response => response.json() as GraphData)
               .catch(this.handleError);
  }

  private handleError(error : any){
    console.error('Erreur ', error);
    return Promise.reject(error.message || error);
  }

}
