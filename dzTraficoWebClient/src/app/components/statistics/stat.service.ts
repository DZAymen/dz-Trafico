import { Injectable } from '@angular/core';
import { Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

@Injectable()
export class StatService {

  private apiURL = 'api/...';


  constructor(private http: Http) { }

  getStat(){
      this.http.get(this.apiURL)
               .toPromise()
               .then()
  }

}
