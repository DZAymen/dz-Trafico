
export const SIDEBAR_ROUTES: SidebarRoute[] = [
    { path: 'map', title: 'Préparer un scénario',  icon:'fa fa-car', class: '' },
    { path: 'realtime', title: 'Simulation en Temps Réel',  icon:'fa fa-clock-o', class: '' },
    { path: 'result', title: 'Résultats & Statistiques',  icon:'fa fa-line-chart', class: '' }
];

 interface SidebarRoute {
    path: string;
    title: string;
    icon: string;
    class: string;
}
