import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs/Rx';
import * as io from 'socket.io-client';
//import { WebsocketService } from './websocket.service';

import 'rxjs/add/operator/toPromise';


export interface Message {
  createSim: boolean
}

@Injectable()
export class CreateSimulationService {

  private  wsURL = 'ws://127.0.0.1:8000/simulation/api/simulationcreation/';
  private socket;

    sendMessage(message) {

      this.socket.emit('add-message', message);
          console.log("MESSAGE SENT");
    }

    getMessages() {
      let observable = new Observable(observer => {

        this.socket = io(this.wsURL);
        this.socket.on('message', (data) => {
          observer.next(data);
        });

        return () => {
          this.socket.disconnect();
        }
      })
      return observable;
    }

    // public createSimulationMsg: Subject<Message>;
    //
  	// constructor() {
    //
  	// }
    //
    // connectToWs(wsService: WebsocketService) {
    // 		return <Subject<Message>>wsService
    // 			.connect(this.wsURL)
    // 			.map((response: MessageEvent): Message => {
    // 				let data = JSON.parse(response.data);
    //         //console.log(data.createSim);
    // 				return data
    // 			});
  	// }


}
