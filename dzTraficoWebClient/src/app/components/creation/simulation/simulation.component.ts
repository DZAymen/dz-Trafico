import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { SimulationConfig } from '../../../domain/simul-config';
import { StartSimulationService } from './start-simulation.service';


@Component({
  selector: 'app-simulation',
  templateUrl: './simulation.component.html',
  styleUrls: ['./simulation.component.css'],
  providers:[StartSimulationService]
})
export class SimulationComponent {

simulConfig = new SimulationConfig();

constructor(
      private router: Router,
      private startSimulationService: StartSimulationService
    ){}

  lancerSimulation(){
      this.startSimulationService.simulationConfig(this.simulConfig);
  }

  prev(){
    this.router.navigate(['/vehicle']);
  }

}
