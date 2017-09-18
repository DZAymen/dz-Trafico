import { Component, OnInit, Input} from '@angular/core';

@Component({
  selector: 'app-speed-limit',
  template: `
            <div class="road-sign">
                <div class="speed-limit">
                  {{speed}}
                </div>
            </div>
          `,
  styles: [`
    .road-sign {
          display: block;
          width: 80px;
          height: 80px;
          background-color: #FFFFFF;
          box-shadow: 5px 5px 2px #888888;
          border: 9px solid #EE0000;
          border-radius: 100px;
          }

    .speed-limit {
          text-align: center;
          padding-top: 30%;
          margin: auto; /*Will center the text*/
          color: #000000;
          font-size: 30px;
          font-weight: bold;
          }
    `]
})
export class SpeedLimitComponent implements OnInit {

    @Input() speed: number;

  constructor() { }

  ngOnInit() {
  }

}
