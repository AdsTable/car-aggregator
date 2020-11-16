import { AfterViewInit, Component, EventEmitter, OnChanges, OnInit, Output, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CarMap, CarService } from '../services/car.service';
import { map, startWith, take } from "rxjs/operators";
import { Observable } from 'rxjs';
import { MatAutocompleteSelectedEvent, MatAutocompleteTrigger } from '@angular/material/autocomplete';

@Component({
  selector: 'search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit, AfterViewInit {

  @ViewChild(MatAutocompleteTrigger) trigger;

  @Output() search: EventEmitter<any> = new EventEmitter();
  availableFields: CarMap;

  brands: string[];
  filteredBrands: Observable<string[]>;

  models: string[];
  filteredModels: Observable<string[]>;

  searchForm: FormGroup;

  constructor(private carService: CarService, private fb: FormBuilder) { 
    this.searchForm = this.fb.group({
      brand: [''],
      model: [{value:'', disabled:true}],
      vin: ['', Validators.pattern(
        '^[A-HJ-NPR-Z\\d]{8}[\\dX][A-HJ-NPR-Z\\d]{2}\\d{6}$')],
    })
  }

  ngOnInit() {
    this.carService.getAvailableFields().pipe(take(1)).subscribe(data => {
      this.availableFields = data;
      this.brands = data.brand.map(v => v.value);
      this.filteredBrands = this.searchForm.get('brand').valueChanges.pipe(
        startWith(''),
        map(value => this._filter(value, this.brands))
      );
    });



  }
  
  brandSelected(e: MatAutocompleteSelectedEvent){
    this.searchForm.controls['model'].setValue(null);
    this.searchForm.controls['model'].enable();

    this.carService.getAvailableModels(e.option.value)
      .pipe(take(1))
      .subscribe(data => {
        this.models = data.map(v => v.value);
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
    console.debug(this.searchForm.value);

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
    this.searchForm.controls['model'].disable();
    this.search.emit({});
  }

  ngOnDestroy() {
    this.trigger.unsubscribe();
  }



  

}
