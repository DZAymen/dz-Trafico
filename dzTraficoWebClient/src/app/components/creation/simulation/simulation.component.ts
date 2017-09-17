import { Component } from '@angular/core';
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
export class SimulationComponent {

  private message = {
    createSim: true
  }
  simulConfig = new SimulationConfig();

constructor(
      private router: Router,
      private startSimulationService: StartSimulationService,
      private createSimulationService: CreateSimulationService
    ){}



    configSimulation(){
        this.startSimulationService.simulationConfig(this.simulConfig);
        //this.sendMsg();
    }

    prev(){
      this.router.navigate(['/vehicle']);
    }

    private sendMsg() {
   		console.log('new message from client to websocket: ', this.message);
   		this.createSimulationService.createSimulationMsg.next(this.message);
   	}


}
