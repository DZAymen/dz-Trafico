import { Component, OnInit, Input, ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';
import {MenuItem} from  'primeng/primeng';

@Component({
  selector: 'app-steps',
  template: '<p-steps [model]="items" [(activeIndex)]="activeIndex" [readonly]="false"></p-steps>',
  styles: [`
        .ui-steps {
          margin-top: 20px;
        }
        .ui-steps .ui-steps-item {
            width: 25%;
        }
        .ui-steps .ui-state-highlight {
            background: #999999;
            color: #FFFFFF;
        }
    `],
    encapsulation: ViewEncapsulation.None
})
export class StepsComponent implements OnInit {

  @Input() activeIndex: number;
  items: MenuItem[];

  constructor(private router: Router) { }

  ngOnInit() {
    this.items = [{
               label: 'Etape 1',
               command: (event: any) => {
                   this.activeIndex = 0;
                   this.router.navigate(['/map']);
               }
           },
           {
               label: 'Etape 2',
               command: (event: any) => {
                   this.activeIndex = 1;
                   this.router.navigate(['/trafficflow']);
               }
           },
           {
               label: 'Etape 3',
               command: (event: any) => {
                   this.activeIndex = 2;
                   this.router.navigate(['/vehicle']);
               }
           },
           {
               label: 'Etape 4',
               command: (event: any) => {
                   this.activeIndex = 3;
                   this.router.navigate(['/start']);
               }
           }
       ];
  }

}