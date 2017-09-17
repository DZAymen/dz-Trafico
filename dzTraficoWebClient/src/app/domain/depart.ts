import { Location } from './location';

export class Depart {
  id: number;
  position: Location;
  departTime: number;
  flow: number;
  order:number;
  constructor(position: Location, departTime: number, flow: number, order:number){
      this.position= position;
      this.departTime= departTime;
      this.flow= flow;
      this.order= order;
  }

}
