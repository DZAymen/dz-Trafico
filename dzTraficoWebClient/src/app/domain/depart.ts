import { Location } from './location';
import { VehicleType } from './vehicle-type';

export class Depart {

   constructor(
          id: number,
          departTime: number,
          from: Location,
          flow: number,
          vehcileType: VehicleType[]
   ){}

}
