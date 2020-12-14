import { Component, OnInit } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import {  Subscription } from 'rxjs';
import { Car } from 'src/app/models/models';
import { CarService } from 'src/app/services/car.service';
import { olderThanWeekAgo } from 'src/app/shared/core';
import { OfferBidComponent } from './offer-bid/offer-bid.component';


@Component({
  selector: 'app-offer-details',
  templateUrl: './offer-details.component.html',
  styleUrls: ['./offer-details.component.scss']
})
export class OfferDetailsComponent implements OnInit {

  private carSubscription: Subscription;
  private carId: number;
  private sub: any;
  car: Car;

  constructor(private route: ActivatedRoute, private carService: CarService, private dialog: MatDialog) { 
  }

  ngOnInit(): void {
    this.sub = this.route.params.subscribe(params => {
      this.carId = +params['id'];
    });

    this.carSubscription = this.carService.getCarById(this.carId).subscribe(item => {
      this.car = item;
    });


  }

  isOld(date: Date) {
    if(olderThanWeekAgo(date)) return true;
    return false;

  }

  openDialog() {
    const dialogConfig = new MatDialogConfig();


    dialogConfig.autoFocus = true;
    dialogConfig.data = this.car;
    dialogConfig.width = "500px"

    this.dialog.open(OfferBidComponent, dialogConfig);
  }

  ngOnDestroy(): void {
    this.sub.unsubscribe();
    this.carSubscription.unsubscribe();
  }

}
