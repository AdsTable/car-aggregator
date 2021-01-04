import { AfterViewInit, Component, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatAutocompleteSelectedEvent, MatAutocompleteTrigger } from '@angular/material/autocomplete';
import { Observable } from 'rxjs';
import { map, startWith, take } from 'rxjs/operators';
import { CarMap } from 'src/app/models/models';
import { CarService } from 'src/app/services/car.service';
import { ShowOnFormInvalidStateMatcher, ProductionInvalidStateMatcher, minLessThanMaxProductionValidator, minLessThanMaxMileageValidator} from '../../shared/validators';


@Component({
  selector: 'offer-filter',
  templateUrl: './offer-filter.component.html',
  styleUrls: ['./offer-filter.component.scss']
})
export class OfferFilterComponent implements OnInit {
  @Input() search: {};
  @Output() filter = new EventEmitter();


  readonly matcher = new ShowOnFormInvalidStateMatcher();
  readonly productionMatcher = new ProductionInvalidStateMatcher();

  brands: string[];
  filteredBrands: Observable<string[]>;

  models: string[];
  filteredModels: Observable<string[]>;

  availableFields: CarMap;
  filterForm: FormGroup;
  multipleValuesField: string[] = ['fuel', 'damage', 'bodyStyle', 'drive', 'transmission']

  usedFilters;


  keyMap = {
    'brand': 'Marka',
    'model': 'Model',
    'vehicle_type': 'Typ pojazdu',
    'bodyStyle': 'Rodzaj nadwozia',
    'year_min': 'Rok prod. od',
    'year_max': 'Rok prod. do',
    'mileage_min': 'Przebieg od',
    'mileage_max': 'Przebieg do',
    'fuel': 'Rodzaj paliwa',
    'damage': 'Uszkodzenie',
    'transmission': 'Skrzynia biegów',
    'drive': 'Napęd'

  }

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
      vehicle_type: [''],
      bodyStyle: [this.search['body_style']],
      year_min: [this.search['year_min']],
      year_max: [this.search['year_max']],
      mileage_min: [this.search['mileage_min'], Validators.min(0)],
      mileage_max: [this.search['mileage_max']],
      fuel: [this.search['fuel']],
      damage: [this.search['damage']],
      transmission: [this.search['transmission']],
      drive: [this.search['drive']],
      auction_site: [''],
      include_closed: [this.search['include_closed']],
    }, {
      validator: [minLessThanMaxMileageValidator, minLessThanMaxProductionValidator]
    })

    this.usedFilters = {
      'brand': this.search['brand'],
      'model': this.search['model'],
      'year_min': this.search['year_min'],
      'year_max': this.search['year_max']
    }

    this.carService.getAvailableFields().pipe(take(1)).subscribe(data => {
      this.availableFields = data;
      this.brands = data.brand;
      this.filteredBrands = this.filterForm.get('brand').valueChanges.pipe(
        startWith(''),
        map(value => this._filter(value, this.brands))
      );
    });
  }



  typeSelected(e: string) {
    this.filterForm.controls['brand'].setValue(null);
    this.filterForm.controls['model'].setValue(null);

    this.carService.getAvailableBrands(e)
      .pipe(take(1))
      .subscribe(data => {
        this.brands = data;
        this.filteredBrands = this.filterForm.get('brand').valueChanges.pipe(
          startWith(''),
          map(value => this._filter(value, this.brands))
        )
      })
  }

  brandSelected(e: MatAutocompleteSelectedEvent) {
    this.filterForm.controls['model'].setValue(null);
    this.filterForm.controls['model'].enable();
  }

  private _filter(value: string, collection: string[]): string[] {
    const filterValue = value?.toUpperCase();
    return collection?.filter(item => item.toUpperCase().startsWith(filterValue));
  }

  prepareFormToSubmit() {
     this.usedFilters = this.filterForm.value;
      if (this.filterForm.get('model').value) {
        this.filterForm.value['model'] = this.filterForm.get('model').value;
      }

      for (let field of this.multipleValuesField) {
        if (this.filterForm.value[field] && Array.isArray(this.filterForm.value[field])) {
          console.log(this.filterForm.value[field]);
          this.filterForm.value[field] = this.filterForm.value[field].join(',');
        }
      }

      const filtered = {};
      for (let key in this.filterForm.value) {
        if (this.filterForm.value[key] || this.filterForm.value[key]===false) {
          filtered[key] = this.filterForm.value[key];
        }
      }

      return filtered;
  }


  onFilter() {
    if (this.filterForm.valid) {
      const filtered = this.prepareFormToSubmit();
      this.filter.emit(filtered);
    }
  }

   resetFilter() {
    for (let [key,value] of Object.entries(this.usedFilters)) {
      if(value) {
        if(key == "include_closed") {
          this.filterForm.controls[key].setValue(false);
        } else {
          this.filterForm.controls[key].setValue(null);
        }
      }
    }
    this.onFilter();
  }

  deleteFilter(key: string) {
    console.log(key);
    this.filterForm.controls[key].setValue(null);
    this.onFilter();
  }

  fillModelsList() {
    console.log('FILL MODELS LIST');
    const brand = this.filterForm.get('brand').value || '';
    const type = this.filterForm.get('vehicle_type').value || '';
    this.carService.getAvailableModels(type, brand)
      .pipe(take(1))
      .subscribe(data => {
        this.models = data;
        this.filteredModels = this.filterForm.get('model').valueChanges.pipe(
          startWith(''),
          map(value => this._filter(value, this.models))
        )
      })
  }


}
