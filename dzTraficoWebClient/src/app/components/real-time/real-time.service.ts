import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs/Rx';
//import { Http } from '@angular/http';
import { WebsocketService } from './websocket.service';
import {RealtimeData} from '../../domain/realtime-data';


export interface Message {
  startSim: boolean
}

@Injectable()
export class RealTimeService {


  private realTimeStateURL ='ws://127.0.0.1:8000/simulation/api/realtimetrafficstate/';
  public startSimulationMsg: Subject<RealtimeData>;



  constructor() {}

  connectToRealTime(wsService: WebsocketService) {
      this.startSimulationMsg =  <Subject<RealtimeData>>wsService
        .connect(this.realTimeStateURL)
        .map((response: MessageEvent): RealtimeData => {
          let data = JSON.parse(response.data);
          return data
        });
  }


  // getTraficState(): Promise<TraficState[]> {
  //      return this.http.get(this.polylineURL)
  //                 .toPromise()
  //                 .then(response => response.json().data as TraficState[])
  //                 .catch(this.handleError);
  // }


  // connectToLc(wsService: WebsocketService) {
  //     this.lcMsg =  <Subject<Lc[]>>wsService
  //       .connect(this.lcURL)
  //       .map((response: MessageEvent): Lc[] => {
  //         let data = JSON.parse(response.data);
  //         return data
  //       });
  // }


}
