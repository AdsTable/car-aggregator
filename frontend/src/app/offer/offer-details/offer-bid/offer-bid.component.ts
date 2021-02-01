import {AfterViewInit, Component, ElementRef, Inject, OnInit, ViewChild} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {Car} from 'src/app/models/models';
import {CarService} from "../../../services/car.service";

@Component({
  selector: 'app-offer-bid',
  templateUrl: './offer-bid.component.html',
  styleUrls: ['./offer-bid.component.scss']
})
export class OfferBidComponent implements OnInit, AfterViewInit {
  carForm: FormGroup;
  car: Car;


  constructor(private fb: FormBuilder,
              private dialogRef: MatDialogRef<OfferBidComponent>, @Inject(MAT_DIALOG_DATA) data,
              private carService: CarService
  ) {
    this.car = data;
  }

  ngOnInit(): void {
    this.carForm = this.fb.group({
      fullname: ['', Validators.required],
      email: ['', [Validators.email, Validators.required]],
      message: ['', Validators.minLength(10)],
      phoneNumber: ['']
    })

  }

  ngAfterViewInit() {
    window.parent.postMessage({'action': 'scroll', 'height': 0}, '*');
  }

  save() {
    if (this.carForm.valid) {
      // TODO: API CALL FOR SENDING MAIL
      const formValue = {
        'car': this.car,
        'form': this.carForm.value
      }
      this.carService.postEmail(formValue).subscribe(data => {
        console.log(data);
      });
      this.dialogRef.close(this.carForm.value);
    }

  }

  close() {
    this.dialogRef.close();
  }

}
