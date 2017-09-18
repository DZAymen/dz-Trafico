import { Component, OnInit } from '@angular/core';
import { StatService } from './stat.service';
import { Result } from '../../domain/result';

@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.css'],
  providers: [StatService]
})
export class StatisticsComponent implements OnInit {

  flowData: any;
  densityData: any;
  resultList: Result[]=[];

  constructor(private statService: StatService) {

   }
     ngOnInit() {
       this.statService.getVariations().then(result => this.resultList = result)

       this.statService.getFlowDiagramData().then(
         graphData => {
           this.drawflowChart(graphData.time, graphData.no_control,graphData.with_control)
         });
        this.statService.getDensityDiagramData().then(
           graphData => {
             this.drawdensityChart(graphData.time, graphData.no_control,graphData.with_control)
        });
     }

   private drawflowChart(x:number[], y1:number[], y2:number[]) {
     this.flowData= {
             labels: x,
             datasets: [
                 {
                     label: 'Sans contrôle',
                     data: y1,
                     fill: false,
                     borderColor: '#4bc0c0'
                 },
                 {
                     label: 'LDV + CV',
                     data: y2,
                     fill: false,
                     borderColor: '#565656'
                 }
             ]
         }
   }

   private drawdensityChart(x:number[], y1:number[], y2:number[]) {
     this.densityData= {
             labels: x,
             datasets: [
                 {
                     label: 'Sans contrôle',
                     data: y1,
                     fill: false,
                     borderColor: '#4bc0c0'
                 },
                 {
                     label: 'LDV + CV',
                     data: y2,
                     fill: false,
                     borderColor: '#565656'
                 }
             ]
         }
   }

}

// this.barData = {
//           labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
//           datasets: [
//               {
//                   label: 'Sans contrôle',
//                   backgroundColor: '#42A5F5',
//                   borderColor: '#1E88E5',
//                   data: [65, 59, 80, 81, 56, 55, 40]
//               },
//               {
//                   label: 'LDV + CV',
//                   backgroundColor: '#9CCC65',
//                   borderColor: '#7CB342',
//                   data: [28, 48, 40, 19, 86, 27, 90]
//               }
//           ]
//       }
