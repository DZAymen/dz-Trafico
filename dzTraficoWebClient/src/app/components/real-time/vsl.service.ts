import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs/Rx';
import { WebsocketService } from './websocket.service';
import {Vsl} from '../../domain/vsl';

@Injectable()
export class VslService {

  private vslURL ='ws://127.0.0.1:8000/simulation/api/vsl/';
  public vslMsg: Subject<Vsl[]> ;

  constructor() { }

  connectToVsl(wsService: WebsocketService) {
      this.vslMsg =  <Subject<Vsl[]>>wsService
        .connect(this.vslURL)
        .map((response: MessageEvent): Vsl[] => {
          let data = JSON.parse(response.data);
          return data
        });
  }
}
