import { Component, OnInit} from '@angular/core';
import {MatDialog, MatDialogConfig} from '@angular/material/dialog';
import {ActivatedRoute} from '@angular/router';
import {Observable, Subscription} from 'rxjs';
import {Car} from 'src/app/models/models';
import {CarService} from 'src/app/services/car.service';
import {olderThanWeekAgo} from 'src/app/shared/core';
import {OfferBidComponent} from './offer-bid/offer-bid.component';
import {MatSnackBar} from "@angular/material/snack-bar";


@Component({
  selector: 'app-offer-details',
  templateUrl: './offer-details.component.html',
  styleUrls: ['./offer-details.component.scss']
})
export class OfferDetailsComponent implements OnInit {

  private carSubscription: Subscription;
  private carId: number;
  private sub: any;
  public activeImage: string;

  similiarCars$: Observable<Car[]>
  car: Car;

  cards = [1, 2, 3, 4]

  constructor(private route: ActivatedRoute, private carService: CarService, private dialog: MatDialog, private snackBar: MatSnackBar) {
  }

  // TODO: FIX THIS, SUBSCRIPTION SHOULDNT BE INSIDE SUBSCIRPTION
  ngOnInit(): void {

    this.sub = this.route.params.subscribe(params => {
      this.carId = +params['id'];
      window.scrollTo(0, 0);
      this.carSubscription = this.carService.getCarById(this.carId).subscribe(item => {
        this.car = item;
        this.activeImage = item.images[0];
      });

      window.parent.postMessage({action: 'scroll', height: 0}, '*');
      this.similiarCars$ = this.carService.getSimiliarById(this.carId);
    });
  }



  isOld(date: Date) {
    return olderThanWeekAgo(date);
  }

  openDialog(event: Car = this.car) {
    const dialogConfig = new MatDialogConfig();

    dialogConfig.autoFocus = true;
    dialogConfig.data = event;
    dialogConfig.width = "500px"
    dialogConfig.position = {top: '10px'}

    const dialogRef = this.dialog.open(OfferBidComponent, dialogConfig);

    dialogRef.afterClosed().subscribe((data) => {
      if (data) {
        this.snackBar.open('Formularz został wysłany', '', {
          duration: 2000,
          horizontalPosition: 'center',
          verticalPosition: "top",
          panelClass: ['mat-toolbar', 'mat-primary']
        });
      }
    });
  }

  ngOnDestroy(): void {
    this.sub.unsubscribe();
    this.carSubscription.unsubscribe();
  }

}
