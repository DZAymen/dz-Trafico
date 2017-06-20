import { VehicleType } from './vehicle-type';

export class VehicleDistribution {
      vehicleType: VehicleType;
      pourcentage: number;

      constructor(vType: VehicleType ){
        this.vehicleType= vType;
        this.pourcentage= 0;
      }
}
