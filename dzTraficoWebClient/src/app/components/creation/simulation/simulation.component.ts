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
  simulConfig = new SimulationConfig();

constructor(
      private router: Router,
      private startSimulationService: StartSimulationService,
      private createSimulationService: CreateSimulationService,
      private wsService: WebsocketService

    ){}



    configSimulation(){
          this.startSimulationService.simulationConfig(this.simulConfig).then( res =>
          this.createSimulationService.connectToWs(this.wsService)
        );

    }

    prev(){
      this.router.navigate(['/vehicle']);
    }




}
