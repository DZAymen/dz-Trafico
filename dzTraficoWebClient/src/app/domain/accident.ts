import { Location } from './location';

export class Accident {
  position: Location;
  lane: number;
  accidentTime: number;
  accidentDuration: number;
constructor(pos: Location, lane:number, accTime: number, accDuration: number){
    this.position=pos;
    this.lane= lane;
    this.accidentTime= accTime;
    this.accidentDuration= accDuration;

}


}
