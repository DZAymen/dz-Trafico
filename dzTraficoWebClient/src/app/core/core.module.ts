import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { SidebarComponent } from './sidebar/sidebar.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule
  ],
  exports: [SidebarComponent],
  declarations: [SidebarComponent],
//  providers: [LoggerService, SpinnerService]  for services
})
export class CoreModule { }
