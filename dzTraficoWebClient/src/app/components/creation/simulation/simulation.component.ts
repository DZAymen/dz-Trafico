import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';

import { SimulationConfig } from '../../../domain/simul-config';
import { StartSimulationService } from './start-simulation.service';
import { CreateSimulationService } from './create-simulation.service';
import { WebsocketService } from './websocket.service';


@Component({
  selector: 'app-simulation',
  templateUrl: './simulation.component.html',
  styleUrls: ['./simulation.component.css'],
  providers:[StartSimulationService, CreateSimulationService, WebsocketService]
})
export class SimulationComponent implements OnInit, OnDestroy {

  simulConfig = new SimulationConfig();
  messages = [];
  connection;
  message;

constructor(
      private router: Router,
      private startSimulationService: StartSimulationService,
      private createSimulationService: CreateSimulationService,
      private wsService: WebsocketService

    ){}


  sendMessage() {
    this.createSimulationService.sendMessage(this.message);
    this.message = '';
  }


  ngOnInit() {
    this.connection = this.createSimulationService.getMessages().subscribe(message => {
      this.messages.push(message);
    })
  }


  ngOnDestroy() {
    this.connection.unsubscribe();
  }

    // private message = {
    // 		createSim: true
    // 	}

      // sendMsg() {
    	// 	console.log('new message from client to websocket: ', this.message);
    	// 	this.createSimulationService.createSimulationMsg.next(this.message);
      //
    	// }

    configSimulation(){
          this.startSimulationService.simulationConfig(this.simulConfig).then( res => {
          // this.createSimulationService.connectToWs(this.wsService).subscribe( res=> {
          //   this.sendMsg() ;
          //   console.log("appel de senMsg")
          // }
          //          )
          //
        });
    }

    prev(){
      this.router.navigate(['/vehicle']);
    }

}
