import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { Car, CarService } from 'src/app/services/car.service';

@Component({
  selector: 'app-home-details',
  templateUrl: './home-details.component.html',
  styleUrls: ['./home-details.component.scss']
})
export class HomeDetailsComponent implements OnInit {

  carId: number;
  private sub: any;
  car$: Observable<Car>;

  constructor(private route: ActivatedRoute, private carService: CarService) { 
  }

  ngOnInit(): void {
    this.sub = this.route.params.subscribe(params => {
      this.carId = +params['id'];
    });

    this.car$ = this.carService.getCarById(this.carId);
  }

  ngOnDestroy(): void {
    this.sub.unsubscribe();
  }

}
