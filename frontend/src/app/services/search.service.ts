import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SearchService {


  searchSubject = new BehaviorSubject(null);

  sendSearchQuery(value: {}) {
    this.searchSubject.next(value);
  }

  resetForm() {
    this.searchSubject.next({});
  }

  
  constructor() { }
}
