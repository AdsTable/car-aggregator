import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, NgForm } from '@angular/forms';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { CarService } from "../services/car.service";
import { olderThanWeekAgo } from '../shared/core';
import { Car } from '../models/models';
import { SearchService } from '../services/search.service';
import { Subscription } from 'rxjs';
import { take } from 'rxjs/operators';
import { MediaChange, MediaObserver } from '@angular/flex-layout';


interface SideNavConfig {
  mode: "over" | "side" | "push"
  opened: boolean;
}

@Component({
  selector: 'app-offer',
  templateUrl: './offer.component.html',
  styleUrls: ['./offer.component.scss']
})
export class OfferComponent implements OnInit {

  @ViewChild('paginator') paginator: MatPaginator;
  @ViewChild('paginatorTop') paginatorTop: MatPaginator;

  searchSubscription: Subscription;
  carSubscription: Subscription;

  loading:boolean = true;

  cars: Car[];

  length: number;
  itemsPerPage: number = 20;
  currentPage: number = 0;
  totalPages: number;

  searchData: {};

  sideNav: SideNavConfig = {
    mode: "side",
    opened: true
  }


  constructor(
    private carService: CarService,
    private searchService: SearchService,
    private mediaObserver: MediaObserver
  ) {
    
    this.mediaObserver.asObservable().subscribe((mediaChange: MediaChange[]) => {
      this.sideNav = this.getSideNavMode(mediaChange);
    }) 
   }



   getSideNavMode(mediaChange: MediaChange[]) {
     if (this.mediaObserver.isActive('gt-sm')) {
        return {
          mode: 'side',
          opened: true
        } as SideNavConfig;
     } 
      return {
        mode: 'over',
        opened: false
      } as SideNavConfig;
     
   }

  ngOnInit(): void {
    this.searchSubscription = this.searchService.searchSubject.pipe(take(1)).subscribe(res => {
      this.searchData = res;
      this.getOffers(this.carService.baseLink, this.createFilterData());
    });

  }

  createFilterData(
    size: number = this.itemsPerPage, 
    page: number = this.currentPage,
    ) {
    return {
      params: {
        'page': page+1,
        'size': size,
        ...this.searchData
      }
    }
  }

  getOffers(url: string, params?) {
    this.loading = true;
    this.carSubscription = this.carService.getCars(url, params).subscribe(page => {
      this.cars = page.results;
      this.length = page.count;

      this.currentPage = page.page;
      this.totalPages = page.lastPage;
      this.loading=false;

    });
  }

  isOld(date: Date) {
    if(olderThanWeekAgo(date)) return true;
    return false;

  }

  pageChangeEvent(event: PageEvent) {

    this.currentPage = event.pageIndex;
    this.itemsPerPage = +event.pageSize;
    this.paginatorTop.pageIndex = this.currentPage;
    this.paginator.pageIndex = this.currentPage;
    this.getOffers(this.carService.baseLink, this.createFilterData());
    window.scroll(0,0);
  }

  onFilter(event) {
    if (this.sideNav.mode === "over") this.sideNav.opened=false;
    console.log(event);
    this.currentPage = 0;
    this.searchData = event;
    this.paginator.firstPage();
    this.getOffers(this.carService.baseLink, this.createFilterData())
  }

  ngOnDestroy() {
    this.searchSubscription.unsubscribe();
    this.carSubscription.unsubscribe();
  }

  




}
