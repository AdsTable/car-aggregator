import { Injectable } from '@angular/core';
import { BehaviorSubject, ReplaySubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SearchService {


  searchSubject = new ReplaySubject<{}>(1);

  sendSearchQuery(value: {}) {
    this.searchSubject.next(value);
  }

  resetForm() {
    this.searchSubject.next({});
  }

  
  constructor() { }
}
