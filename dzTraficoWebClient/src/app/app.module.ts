import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { SidebarModule } from 'ng-sidebar';
import { GMapModule, InputTextModule, ButtonModule, GrowlModule, DropdownModule, DialogModule,
         SpinnerModule, SliderModule, DataTableModule, ChartModule, PanelModule, ConfirmDialogModule
       }  from 'primeng/primeng';

// Imports for loading & configuring the in-memory web api
import { InMemoryWebApiModule } from 'angular-in-memory-web-api';
import { TrafficFlowData }  from './data/trafficflow-data';


// Feature Components
import { AppComponent } from './app.component';
import { MapComponent } from './components/creation/map/map.component';
import { TrafficComponent } from './components/creation/traffic/traffic.component';
import { VehicleComponent } from './components/creation/vehicle/vehicle.component';
import { SimulationComponent } from './components/creation/simulation/simulation.component';

// Other Modules
import { SharedModule } from './shared/shared.module';
import { CoreModule } from './core/core.module';

// Routing
import {routing} from './app.routing';
import { StatisticsComponent } from './components/result/statistics/statistics.component';



@NgModule({
  declarations: [
    AppComponent,
    MapComponent,
    TrafficComponent,
    VehicleComponent,
    SimulationComponent,
    StatisticsComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    HttpModule,
    InMemoryWebApiModule.forRoot(TrafficFlowData),


    SharedModule, CoreModule,
    routing,
    SidebarModule.forRoot(),
    GMapModule, InputTextModule, ButtonModule, GrowlModule, DropdownModule, DialogModule,
    SpinnerModule, SliderModule, DataTableModule, ChartModule, PanelModule, ConfirmDialogModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
