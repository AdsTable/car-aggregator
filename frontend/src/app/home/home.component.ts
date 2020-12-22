import { Component, OnInit, ViewChild } from '@angular/core';
import { MediaChange, MediaObserver } from '@angular/flex-layout';
import { Router } from '@angular/router';
import { CarService } from "../services/car.service";
import { SearchService } from '../services/search.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  hotBrands = [
               'BMW', 'AUDI', 'PORSCHE', 'NISSAN', 'VOLKSWAGEN', 
               'OPEL', 'KIA', 'CHEVROLET', 'DODGE', 'FORD', 
               'HONDA', 'JEEP', 'TOYOTA', 'FIAT', 'RENAULT', 'HYUNDAI'
              ]
  gridCols = 8;

  constructor(private mediaObserver: MediaObserver, private searchService: SearchService, private router: Router) {
    this.mediaObserver.asObservable().subscribe((mediaChange: MediaChange[]) => {
      this.gridCols = this.getGridCols();
    }) 
   }

   getGridCols() {
     if(this.mediaObserver.isActive('gt-md')) {
       return 8;
     } else if(this.mediaObserver.isActive('lt-sm')) {
       return 2;
     } else {
       return 4;
     }
   }

   clickPopularBrand(brand:string) {
    this.searchService.sendSearchQuery({'brand': brand, 'include_closed':false});
    this.router.navigate(['/offers'])
   }


  ngOnInit(): void {

  }

 
}
