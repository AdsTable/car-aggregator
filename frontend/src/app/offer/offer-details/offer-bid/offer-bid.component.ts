import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Car } from 'src/app/models/models';

@Component({
  selector: 'app-offer-bid',
  templateUrl: './offer-bid.component.html',
  styleUrls: ['./offer-bid.component.scss']
})
export class OfferBidComponent implements OnInit {

  carForm: FormGroup;
  car: Car;

  constructor(private fb: FormBuilder,
    private dialogRef: MatDialogRef<OfferBidComponent>, @Inject(MAT_DIALOG_DATA) data) { 
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

  save() {
    if (this.carForm.valid) {
      // TODO: API CALL FOR SENDING MAIL
      this.dialogRef.close(this.carForm.value);
    }

  }

  close() {
    this.dialogRef.close();
  }

}
