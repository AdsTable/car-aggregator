import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, NgForm } from '@angular/forms';
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

  orderBy;
  orderList = [
    {icon: 'arrow_drop_down', name: 'Current Price', value: '-current_price'},
    {icon: 'arrow_drop_up', name: 'Current Price', value: 'current_price'},

    {icon: 'arrow_drop_down', name: 'Data licytacji', value: '-sale_date'},
    {icon: 'arrow_drop_up', name: 'Data licytacji', value: 'sale_date'},

    {icon: 'arrow_drop_down', name: 'Przebieg', value: '-mileage'},
    {icon: 'arrow_drop_up', name: 'Przebieg', value: 'mileage'},

    {icon: 'arrow_drop_down', name: 'Rocznik', value: '-production_year'},
    {icon: 'arrow_drop_up', name: 'Rocznik', value: 'production_year'},
  ]

  sideNav: SideNavConfig = {
    mode: "side",
    opened: true
  }

  hidePageSize: boolean = false;


  constructor(
    private carService: CarService,
    private searchService: SearchService,
    private mediaObserver: MediaObserver
  ) {
    
    this.mediaObserver.asObservable().subscribe((mediaChange: MediaChange[]) => {
      this.sideNav = this.getSideNavMode(mediaChange);
      this.hidePageSize = this.getHidePageSize(mediaChange);
    }) 
   }


   getHidePageSize(mediaChange) {
     if (this.mediaObserver.isActive('gt-sm')){
       return false;
     }
     return true;
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
    this.orderBy = this.orderList[2];

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
        'ordering': this.orderBy.value,
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
    this.currentPage = 0;
    this.searchData = event;
    this.paginator.firstPage();
    this.getOffers(this.carService.baseLink, this.createFilterData())
  }

  onOrderChange() {
    this.currentPage = 0;
    this.paginator.firstPage();
    this.getOffers(this.carService.baseLink, this.createFilterData());

  }

  ngOnDestroy() {
    this.searchSubscription.unsubscribe();
    this.carSubscription.unsubscribe();
  }

  




}
