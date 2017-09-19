
export const SIDEBAR_ROUTES: SidebarRoute[] = [
    { path: 'map', title: 'Scénario de simulation',  icon:'fa fa-car', class: '' },
    { path: 'realtime', title: 'Exécution de la simulation',  icon:'fa fa-clock-o', class: '' },
    { path: 'result', title: 'Résultats & Statistiques',  icon:'fa fa-line-chart', class: '' }
];

 interface SidebarRoute {
    path: string;
    title: string;
    icon: string;
    class: string;
}
