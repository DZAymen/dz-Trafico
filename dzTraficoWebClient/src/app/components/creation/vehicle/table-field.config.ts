
export const DATATABLE_FIELD: DataTableField[] = [
  {field: 'vehicleType.id', header: 'Model'},
  {field: 'vehicleType.length', header: 'Longueur'},
  {field: 'vehicleType.width', header: 'Largeur'},
  {field: 'vehicleType.height', header: 'Hauteur'},
  {field: 'vehicleType.minGap', header: 'Min gap'},
  {field: 'vehicleType.acceleration', header: 'Accélération'},
  {field: 'vehicleType.deceleration', header: 'Décélération'},
  {field: 'vehicleType.maxSpeed', header: 'Max speed'},
];

 interface DataTableField{
    field: string;
    header: string;
}
