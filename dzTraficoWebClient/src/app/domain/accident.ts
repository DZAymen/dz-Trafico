import { Location } from './location';

export class Accident {
  position: Location;
  accidentTime: number;
  accidentDuration: number;
constructor(pos: Location, accTime: number, accDuration: number){
    this.position=pos;
    this.accidentTime= accTime;
    this.accidentDuration= accDuration;

}


}
