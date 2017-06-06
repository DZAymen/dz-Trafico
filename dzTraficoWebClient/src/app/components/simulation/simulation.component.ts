import { Component, OnInit } from '@angular/core';
import { StartSimulationService } from './start-simulation.service';


@Component({
  selector: 'app-simulation',
  templateUrl: './simulation.component.html',
  styleUrls: ['./simulation.component.css'],
  providers:[StartSimulationService]
})
export class SimulationComponent implements OnInit {

  data: any;

  constructor() {
    this.data= {
      labels:['type A', 'type B', 'type C'],
      datasets: [
        {
          data:[300, 50, 100],
          backgroundColor: [
            "#FF6384",
            "#36A2EB",
            "#FFCE56"
          ],
          hoverBackgroundColor: [
            "#FF6384",
            "#36A2EB",
            "#FFCE56"
          ]
        }

      ]
    }
   }

  ngOnInit() {
  }

}
