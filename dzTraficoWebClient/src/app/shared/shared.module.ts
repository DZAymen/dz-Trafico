import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StepsModule } from 'primeng/primeng';

import { HeaderComponent } from './header/header.component';
import { StepsComponent } from './steps/steps.component';

@NgModule({
  imports: [
    CommonModule,
    StepsModule
  ],
  declarations: [HeaderComponent, StepsComponent],
  exports:[
    CommonModule,
    HeaderComponent,
    StepsComponent
  ]
})
export class SharedModule { }
