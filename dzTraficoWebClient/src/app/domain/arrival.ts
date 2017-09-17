import { Location } from './location';

export class Arrival {
      position: Location;
      percentage: number;
      order:number;
  constructor(pos: Location, percentage:number, order: number){
    this.position= pos;
    this.percentage=percentage;
    this.order= order;
  }

}
