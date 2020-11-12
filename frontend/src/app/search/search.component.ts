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
    if (this.searchForm.valid) {
      this.search.emit(this.searchForm.value);
    }
  }

  resetForm() {
    this.searchForm.reset();
    this.search.emit(this.searchForm.value);
  }

}
