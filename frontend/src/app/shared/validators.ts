import { ErrorStateMatcher } from '@angular/material/core';
import { FormBuilder, FormControl, FormGroup, FormGroupDirective, ValidationErrors, Validators } from '@angular/forms';


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
  
  export function minLessThanMaxMileageValidator(group: FormGroup): ValidationErrors | null {
    const minMileage = group.controls['mileage_min'].value;
    const maxMileage = group.controls['mileage_max'].value;
  
    if (minMileage && maxMileage) {
      return minMileage <= maxMileage ? null : { minLessThanMaxMileage: true };
    } else {
      return null;
    }
  }
  
  export function minLessThanMaxProductionValidator(group: FormGroup): ValidationErrors | null {
    const minYear = group.controls['year_min'].value;
    const maxYear = group.controls['year_max'].value;
  
    if (minYear && maxYear) {
      return minYear <= maxYear ? null : { minLessThanMaxProduction: true };
    } else {
      return null;
    }
  }