import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { SidebarModule } from 'ng-sidebar';
import { GMapModule, InputTextModule, ButtonModule, GrowlModule, DropdownModule, DialogModule,
         SpinnerModule, SliderModule, DataTableModule, ChartModule
       }  from 'primeng/primeng';

// Feature Components
import { AppComponent } from './app.component';
import { MapComponent } from './components/map/map.component';
import { TrafficComponent } from './components/traffic/traffic.component';
import { VehicleComponent } from './components/vehicle/vehicle.component';

// Other Modules
import { SharedModule } from './shared/shared.module'

// Routing
import {routing} from './app.routing';
import { SimulationComponent } from './components/simulation/simulation.component';


@NgModule({
  declarations: [
    AppComponent,
    MapComponent,
    TrafficComponent,
    VehicleComponent,
    SimulationComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpModule,

    SharedModule,
    routing,
    SidebarModule.forRoot(),
    GMapModule, InputTextModule, ButtonModule, GrowlModule, DropdownModule, DialogModule,
    SpinnerModule, SliderModule, DataTableModule, ChartModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
