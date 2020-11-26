import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { take } from 'rxjs/operators';
import { CarMap } from 'src/app/models/models';
import { CarService } from 'src/app/services/car.service';
import { SearchService } from 'src/app/services/search.service';

@Component({
  selector: 'offer-filter',
  templateUrl: './offer-filter.component.html',
  styleUrls: ['./offer-filter.component.scss']
})
export class OfferFilterComponent implements OnInit {
  @Input() search: {};
  @Output() filter = new EventEmitter();

  availableFields: CarMap;
  filterForm: FormGroup;
  multipleValuesField: string[] = ['fuel', 'damage', 'bodyStyle']


  constructor(private carService: CarService, private fb: FormBuilder) { 

  }

  ngOnInit(): void {
    for (let field of this.multipleValuesField) {
      if (this.search[field]) {
        this.search[field] = this.search[field].split(',');
      }
    }
    this.filterForm = this.fb.group({
      brand: [this.search['brand']],
      model: [this.search['model']],
      vehicle_type: [],
      location: [],
      bodyStyle: [this.search['body_style']],
      year_min: [this.search['year_min']],
      year_max: [this.search['year_max']],
      mileage_min: [this.search['mileage_min']],
      mileage_max: [this.search['mileage_max']],
      fuel: [this.search['fuel']],
      damage: [this.search['damage']],
      transmission: [this.search['transmission']]
    })

    this.carService.getAvailableFields().pipe(take(1)).subscribe(data => {
      this.availableFields = data;
    });
  }


  // onFilter(): void {
  //   console.log(this.filterForm.value);
  // }

  onFilter() {
    if (this.filterForm.valid) {

      for (let field of this.multipleValuesField) {
        if (this.filterForm.value[field]) {
          this.filterForm.value[field] = this.filterForm.value[field].join(',');
        }
      }

      const filtered = {};
      for (let key in this.filterForm.value) {
        if (this.filterForm.value[key]) {
          filtered[key] = this.filterForm.value[key];
        }
      }

 
      this.filter.emit(filtered);
    }

  }
}
