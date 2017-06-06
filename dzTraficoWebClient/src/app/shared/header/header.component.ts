import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-header',
  template: `
    <div class="title-block">
        <div>
            <span class="title-text">{{title}}</span>
            <span>{{description}}</span>
        </div>
    </div>`,
  styles: [`
  .title-block{
      display: block;
      border-bottom: solid 1px #dde3e6;
      padding: 14px 24px;
      background-color: #f5f7f8;
  }
  .title-text {
      font-size: 30px;
      margin-bottom: 20px;
      display: block;
      color: #2590ec;
  }
  `]
})
export class HeaderComponent {

    @Input() title: string;
    @Input() description : string;

}
