import { Location } from './location';

export class Depart {
  position: Location;
  departTime: number;
  flow: number;
  constructor(position: Location, departTime: number, flow: number){
      this.position= position;
      this.departTime= departTime;
      this.flow= flow;
  }

}
