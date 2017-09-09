import {ModuleWithProviders} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';


import {MapComponent} from './components/creation/map/map.component';
import {TrafficComponent} from './components/creation/traffic/traffic.component';
import {VehicleComponent} from './components/creation/vehicle/vehicle.component';
import {SimulationComponent} from './components/creation/simulation/simulation.component';
import {RealTimeComponent} from './components/real-time/real-time.component';
import {StatisticsComponent} from './components/statistics/statistics.component';

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
  },
  {
    path: 'realtime',
    component: RealTimeComponent
  },
  {
    path: 'result',
    component: StatisticsComponent
  },
   // { path: '**', component: PageNotFoundComponent }
  {
    path: '',
    redirectTo: 'map',
    pathMatch: 'full' }
];
export const routing: ModuleWithProviders = RouterModule.forRoot(appRoutes);
