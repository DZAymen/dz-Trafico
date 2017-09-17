import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StepsModule } from 'primeng/primeng';

import { OsmService } from './osm.service';
import { StepsComponent } from './steps/steps.component';
import { SpeedLimitComponent } from './speed-limit/speed-limit.component';



@NgModule({
  imports: [
    CommonModule,
    StepsModule
  ],
  declarations: [StepsComponent, SpeedLimitComponent],
  exports:[
    CommonModule,
    StepsComponent,
    SpeedLimitComponent
  ],
  providers: [OsmService]
})
export class SharedModule { }
