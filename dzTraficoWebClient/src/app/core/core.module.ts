import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ButtonModule } from 'primeng/primeng';

import { SidebarComponent } from './sidebar/sidebar.component';
import { ToolbarComponent } from './toolbar/toolbar.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    ButtonModule
  ],
  exports: [SidebarComponent,
     ToolbarComponent],
  declarations: [
    SidebarComponent,
    ToolbarComponent
  ],
//  providers: [LoggerService, SpinnerService]  for services
})
export class CoreModule { }
