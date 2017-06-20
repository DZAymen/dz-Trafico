import { Component,EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-toolbar',
  template: `<div class="on-map">
               <button type="button" pButton icon="fa-flag" (click)="dialogType('depart')"></button>
               <button type="button" pButton icon="fa-flag-checkered" class="ui-button-warning" (click)="dialogType('')"></button>
               <button type="button" pButton icon="fa-car" class="ui-button-success" (click)="dialogType('accident')"></button>
               <button type="button" pButton icon="fa-trash" class="ui-button-danger" (click)="remove()"></button>
             </div>`,
  styles: [`
    .on-map {
        position: absolute;
        margin-top: 10px;
        margin-left: 10px;
        z-index: 100;
    }
    `]
})
export class ToolbarComponent {

  removing: boolean= false;
  @Output() dialogToShow  = new EventEmitter<string>();
  @Output() removeMarker = new EventEmitter<boolean>();

  dialogType(type: string){
    this.dialogToShow.emit(type);
  }

  remove(){
    this.removing= !this.removing;
    this.removeMarker.emit(this.removing)
  }
}
