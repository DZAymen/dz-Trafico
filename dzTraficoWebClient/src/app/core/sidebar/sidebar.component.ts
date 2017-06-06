import { Component, OnInit } from '@angular/core';
import { SIDEBAR_ROUTES } from './sidebar-routes.config';

//declare var $:any;
@Component({
    moduleId: module.id,
    selector: 'sidebar-cmp',
    templateUrl: 'sidebar.component.html',

})

export class SidebarComponent implements OnInit {
    menuItems: any[];

    ngOnInit() {
      //  $.getScript('../../../assets/js/sidebar-moving-tab.js');
        this.menuItems = SIDEBAR_ROUTES.filter(menuItem => menuItem);
    }
}
