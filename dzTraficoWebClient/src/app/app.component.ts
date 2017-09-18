import { Component, OnInit, AnimationTransitionEvent } from '@angular/core';


@Component({
  moduleId: module.id,
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],

})
export class AppComponent implements OnInit{

  private opened: boolean;

  ngOnInit(){
      this.opened=true;
  }

  private toggleOpened(): void {
        this.opened = !this.opened;
  }

}
