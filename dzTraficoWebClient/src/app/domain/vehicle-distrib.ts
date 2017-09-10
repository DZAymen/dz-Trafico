import { VehicleType } from './vehicle-type';

export class VehicleDistribution {
      vehicleType: VehicleType;
      percentage: number;

      constructor(vType: VehicleType ){
        this.vehicleType= vType;
        this.percentage= 0;
      }
}
