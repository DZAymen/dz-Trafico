
export const SIDEBAR_ROUTES: SidebarRoute[] = [
    { path: '', title: 'Dashboard',  icon: 'fa fa-dashboard', class: '' },
    { path: 'map', title: 'Lancer simulation',  icon:'fa fa-car', class: '' },
    { path: '', title: 'Table List',  icon:'fa fa-bars', class: '' }
];

 interface SidebarRoute {
    path: string;
    title: string;
    icon: string;
    class: string;
}
