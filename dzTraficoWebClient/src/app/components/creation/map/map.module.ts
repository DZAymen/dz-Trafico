import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';


import { MapComponent } from './map.component';

@NgModule({
  imports: [
    CommonModule
  ],
  declarations: [MapComponent],
  exports:[
    CommonModule,
    MapComponent,
  ]
})
export class MapModule { }
