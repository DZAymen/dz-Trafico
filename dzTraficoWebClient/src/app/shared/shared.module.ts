import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StepsModule } from 'primeng/primeng';

import { OsmService } from './osm.service';
import { StepsComponent } from './steps/steps.component';



@NgModule({
  imports: [
    CommonModule,
    StepsModule
  ],
  declarations: [StepsComponent],
  exports:[
    CommonModule,
    StepsComponent
  ],
  providers: [OsmService]
})
export class SharedModule { }
