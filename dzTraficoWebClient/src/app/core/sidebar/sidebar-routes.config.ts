
export const SIDEBAR_ROUTES: SidebarRoute[] = [
    { path: '', title: 'Tableau de Bord',  icon: 'fa fa-dashboard', class: '' },
    { path: 'map', title: 'Lancer simulation',  icon:'fa fa-car', class: '' },
    { path: '', title: 'Simulation en Temps Réel',  icon:'fa fa-clock-o', class: '' },
    { path: 'result', title: 'Résultat Simulation',  icon:'fa fa-line-chart', class: '' }
];

 interface SidebarRoute {
    path: string;
    title: string;
    icon: string;
    class: string;
}
