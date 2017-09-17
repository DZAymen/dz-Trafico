import { Location } from './location';

export class Depart {
  id: number;
  position: Location;
  departTime: number;
  flow: number;
  outs:[0]
  constructor(position: Location, departTime: number, flow: number){
      this.position= position;
      this.departTime= departTime;
      this.flow= flow;
  }

}
