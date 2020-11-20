import { AfterViewInit, Component, EventEmitter, OnChanges, OnInit, Output, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, FormGroupDirective, ValidationErrors, Validators } from '@angular/forms';
import { CarMap } from '../models/models';
import { map, startWith, take } from "rxjs/operators";
import { Observable } from 'rxjs';
import { MatAutocompleteSelectedEvent, MatAutocompleteTrigger } from '@angular/material/autocomplete';
import { CarService } from '../services/car.service';
import { SearchService } from '../services/search.service';
import { ErrorStateMatcher } from '@angular/material/core';
import { Router } from '@angular/router';

@Component({
  selector: 'search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit, AfterViewInit {

  @ViewChild(MatAutocompleteTrigger) trigger;

  readonly matcher = new ShowOnFormInvalidStateMatcher();
  readonly productionMatcher = new ProductionInvalidStateMatcher();

  availableFields: CarMap;

  brands: string[];
  filteredBrands: Observable<string[]>;

  models: string[];
  filteredModels: Observable<string[]>;


  searchForm: FormGroup;

  multipleValuesField: string[] = ['fuel', 'damage', 'bodyStyle']

  constructor(private carService: CarService, 
    private searchService: SearchService, 
    private fb: FormBuilder,
    private router: Router) {
    this.searchForm = this.fb.group({
      brand: [''],
      model: [{ value: '', disabled: true }],
      vin: ['', Validators.pattern(
        '^[A-HJ-NPR-Z\\d]{8}[\\dX][A-HJ-NPR-Z\\d]{2}\\d{6}$')],
      year_min: [''],
      year_max: [''],
      mileage_min: ['', Validators.min(0)],
      mileage_max: [''],
      fuel: [''],
      damage: [''],
      transmission: [''],
      bodyStyle: ['']
    }, {
      validator: [minLessThanMaxMileageValidator, minLessThanMaxProductionValidator]
    })
  }

  ngOnInit() {
    this.carService.getAvailableFields().pipe(take(1)).subscribe(data => {
      this.availableFields = data;
      this.brands = data.brand;
      this.filteredBrands = this.searchForm.get('brand').valueChanges.pipe(
        startWith(''),
        map(value => this._filter(value, this.brands))
      );
    });
  }


  brandSelected(e: MatAutocompleteSelectedEvent) {
    this.searchForm.controls['model'].setValue(null);
    this.searchForm.controls['model'].enable();

    this.carService.getAvailableModels(e.option.value)
      .pipe(take(1))
      .subscribe(data => {
        this.models = data;
        this.filteredModels = this.searchForm.get('model').valueChanges.pipe(
          startWith(''),
          map(value => this._filter(value, this.models))
        )
      })
  }

  ngAfterViewInit() {
    this.trigger.panelClosingActions
      .subscribe(e => {
        if (!(e && e.source)) {
          this.searchForm.controls['brand'].setValue(null);
          this.searchForm.controls['model'].setValue(null);
          this.searchForm.controls['model'].disable();
          this.trigger.closePanel();
        }
      });
  }


  private _filter(value: string, collection: string[]): string[] {
    const filterValue = value?.toUpperCase();
    return collection?.filter(item => item.toUpperCase().startsWith(filterValue));
  }

  onSearch() {
    if (this.searchForm.valid) {

      for (let field of this.multipleValuesField) {
        if (this.searchForm.value[field]) {
          this.searchForm.value[field] = this.searchForm.value[field].join(',');
        }
      }

      const filtered = {};
      for (let key in this.searchForm.value) {
        if (this.searchForm.value[key]) {
          filtered[key] = this.searchForm.value[key];
        }
      }

 
      this.searchService.sendSearchQuery(filtered);
      this.router.navigate(['/offers'])
    }

  }

  resetForm() {
    this.searchForm.reset();
    this.searchForm.controls['model'].disable();
    this.searchService.resetForm();
  }

  ngOnDestroy() {
  }


}

export class ShowOnFormInvalidStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective): boolean {
    return !!((control && control.invalid) || (form && form.hasError('minLessThanMaxMileage')));
  }
}

export class ProductionInvalidStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective): boolean {
    return !!((control && control.invalid) || (form && form.hasError('minLessThanMaxProduction')));
  }
}

function minLessThanMaxMileageValidator(group: FormGroup): ValidationErrors | null {
  const minMileage = group.controls['mileage_min'].value;
  const maxMileage = group.controls['mileage_max'].value;

  if (minMileage && maxMileage) {
    return minMileage <= maxMileage ? null : { minLessThanMaxMileage: true };
  } else {
    return null;
  }
}

function minLessThanMaxProductionValidator(group: FormGroup): ValidationErrors | null {
  const minYear = group.controls['year_min'].value;
  const maxYear = group.controls['year_max'].value;

  if (minYear && maxYear) {
    return minYear <= maxYear ? null : { minLessThanMaxProduction: true };
  } else {
    return null;
  }
}

