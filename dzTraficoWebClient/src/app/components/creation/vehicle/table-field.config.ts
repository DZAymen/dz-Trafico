
export const DATATABLE_FIELD: DataTableField[] = [
  {field: 'vehicleType.id', header: 'Model'},
  {field: 'vehicleType.accel', header: 'Accel'},
  {field: 'vehicleType.decel', header: 'Decel'},
  {field: 'vehicleType.impatience', header: 'Impatience'},
  {field: 'vehicleType.sigma', header: 'sigma'},
  {field: 'vehicleType.minGap', header: 'MinGap'},
  {field: 'vehicleType.tau', header: 'Tau'},
  {field: 'vehicleType.maxSpeed', header: 'MaxSpeed'},
];

 interface DataTableField{
    field: string;
    header: string;

}
