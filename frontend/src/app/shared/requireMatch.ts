import { AbstractControl, ValidatorFn } from '@angular/forms';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export function RequireMatch(control: AbstractControl, options: string[]) {
    const selection: any = control.value;

    if (typeof selection === 'string') {
        return { incorrect: true };
    }
    return null;
}

// export function autocompleteStringValidator(exists: (validOptions: string[]) => boolean): ValidatorFn {
//     if (exists(validOptions)) {

//     }
//     return (control: AbstractControl): { [key: string]: any} | null {
//         if (validOptions.includes(control.value)) {
//             return null;
//         }
//         return {incorrect: true};
//     }
// }


export function autoCompleteValidator(validOptions: Observable<string[]>, control: AbstractControl) {
    const value = control.value.toUpperCase();

    return validOptions.pipe(
        map(items => items.filter(b => b.toLowerCase() === value)),
        map(items => items.length ? null : { incorrect: true })
    );
}


export function AutoUnsub() {
    return function(constructor) {
        const orig = constructor.prototype.ngOnDestroy
        constructor.prototype.ngOnDestroy = function() {
            for(const prop in this) {
                console.log(prop);
                const property = this[prop]
                if(typeof property.subscribe === "function") {
                    console.log(property);
                    property.unsubscribe()
                }
            }
            orig.apply()
        }
    }
}


