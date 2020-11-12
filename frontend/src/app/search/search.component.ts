import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent {

  @Output() search: EventEmitter<any> = new EventEmitter();

  searchForm: FormGroup;

  constructor(private fb: FormBuilder) { 
    this.searchForm = this.fb.group({
      'brand': [''],
      'model': [''],
    })
  }

  onSearch() {
    const filtered = {};
    if (this.searchForm.valid) {
      for (let key in this.searchForm.value) {
        if (this.searchForm.value[key]) {
          filtered[key] = this.searchForm.value[key];
        }
      }
      this.search.emit(filtered);
    }
  }

  resetForm() {
    this.searchForm.reset();
    this.search.emit({});
  }


  

}
