import { Location } from './location';

export class Arrival {
      position: Location;
      percentage: number;
  constructor(pos: Location, percentage:number){
    this.position= pos;
    this.percentage=percentage;
  }

}
