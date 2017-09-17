import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs/Rx';
import { Http } from '@angular/http';
import { WebsocketService } from './websocket.service';


import {TraficState} from '../../domain/trafic-state';


export interface Message {
  startSim: boolean
}

@Injectable()
export class RealTimeService {


  private realTimeStateURL ='ws://127.0.0.1:8000/simulation/api/realtimetrafficstate/';
  public startSimulationMsg: Subject<Message>;



  constructor(private http: Http) {}

  connectToRealTime(wsService: WebsocketService) {
      this.startSimulationMsg =  <Subject<Message>>wsService
        .connect(this.realTimeStateURL)
        .map((response: MessageEvent): Message => {
          let data = JSON.parse(response.data);
          return data
        });
  }



  // connectToLc(wsService: WebsocketService) {
  //     this.lcMsg =  <Subject<Lc[]>>wsService
  //       .connect(this.lcURL)
  //       .map((response: MessageEvent): Lc[] => {
  //         let data = JSON.parse(response.data);
  //         return data
  //       });
  // }


}
