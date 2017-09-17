import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { GraphData } from '../../domain/graph-data';
import { Result } from '../../domain/result';

@Injectable()
export class StatService {

  private apiURL = 'api/diagramData';
  private resultURL = 'api/result';

  constructor(private http: Http) { }

  getVariations(): Promise<Result[]>{
    return  this.http.get(this.resultURL)
               .toPromise()
               .then(response => response.json().data as Result[])
               .catch(this.handleError);
  }

  getDiagramData(): Promise<GraphData>{
      return this.http.get(this.apiURL)
               .toPromise()
               .then(response => response.json().data as GraphData)
               .catch(this.handleError);
  }


  private handleError(error : any){
    console.error('Erreur ', error);
    return Promise.reject(error.message || error);
  }

}
