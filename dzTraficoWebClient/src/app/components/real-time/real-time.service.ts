import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs/Rx';
import { Http } from '@angular/http';
import { WebsocketService } from './websocket.service';

import 'rxjs/add/operator/toPromise';

import {Lc} from '../../domain/lc';
import {Vsl} from '../../domain/vsl';
import {TraficState} from '../../domain/trafic-state';


export interface Message {
  startSim: boolean
}

@Injectable()
export class RealTimeService {

  //private lcURL = 'ws://127.0.0.1:8000/simulation/api/lcrecommendations/';
  private realTimeStateURL ='ws://127.0.0.1:8000/simulation/api/realtimetrafficstate/';
  private lcURL= "api/recommandationTest";
  private vslURL= "api/vslTest";
  private polylineURL="api/polyline";

  // public recommandations: Subject<Lc>;
  //
  // 	constructor(wsService: WebsocketService) {
  //   		this.recommandations = <Subject<Lc>>wsService
  //   			.connect(this.lcURL)
  //   			.map((response: MessageEvent): Lc => {
  //   				let data = JSON.parse(response.data);
  //   				return data
  //   			});
  // 	}

  private  wsURL = 'ws://127.0.0.1:8000/simulation/api/simulationcreation/';


  public startSimulationMsg: Subject<Message>;


  constructor(private http: Http) {}


  connectToWs(wsService: WebsocketService) {
      this.startSimulationMsg =  <Subject<Message>>wsService
        .connect(this.wsURL)
        .map((response: MessageEvent): Message => {
          let data = JSON.parse(response.data);
          return data
        });
  }

  getRecommandation(): Promise<Lc[]> {
     return this.http.get(this.lcURL)
                .toPromise()
                .then(response => response.json().data as Lc[])
                .catch(this.handleError);
  }


  getVsl(): Promise<Vsl[]> {
       return this.http.get(this.vslURL)
                  .toPromise()
                  .then(response => response.json().data as Vsl[])
                  .catch(this.handleError);
  }

  getTraficState(): Promise<TraficState[]> {
       return this.http.get(this.polylineURL)
                  .toPromise()
                  .then(response => response.json().data as TraficState[])
                  .catch(this.handleError);
  }



  private handleError(error : any){
    console.error('Erreur ', error);
    return Promise.reject(error.message || error);
  }

}
