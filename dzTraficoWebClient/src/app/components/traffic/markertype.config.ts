
export const MARKER_TYPES: MarkerType[] = [
    {label: 'Point d\'entré', value: 'depart'},
    {label: 'Point de sortie', value: 'arrival'},
    {label: 'Accident', value: 'accident'}
];

 interface MarkerType {
    label: string;
    value: string;
}
