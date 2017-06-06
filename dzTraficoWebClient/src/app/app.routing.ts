import {ModuleWithProviders} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';


import {MapComponent} from './components/map/map.component';
import {TrafficComponent} from './components/traffic/traffic.component';
import {VehicleComponent} from './components/vehicle/vehicle.component';
import {SimulationComponent} from './components/simulation/simulation.component';

const appRoutes: Routes = [
  {
    path: 'map',
    component: MapComponent
  },
  {
    path: 'vehicle',
    component: VehicleComponent
  },
  {
    path: 'trafficflow',
    component: TrafficComponent
  },
  {
    path: 'start',
    component: SimulationComponent
  }
   // { path: '**', component: PageNotFoundComponent }
   // { path: '', redirectTo: 'dashboard', pathMatch: 'full' }
];
export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);
