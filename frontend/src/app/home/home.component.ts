import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, NgForm } from '@angular/forms';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { Observable, range } from 'rxjs';
import { filter, map, tap, toArray } from "rxjs/operators";
import { CarService, Page, Car } from "../services/car.service";
import { olderThanWeekAgo } from '../shared/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  @ViewChild('paginator') paginator: MatPaginator;

  loading:boolean = true;

  cars: Car[];

  length: number;
  itemsPerPage: number = 20;
  currentPage: number = 1;
  totalPages: number;

  searchData: {};

  constructor(private carService: CarService, private fb: FormBuilder) { }

  ngOnInit(): void {
    this.getOffers(this.carService.baseLink, this.createFilterData());
  }

  createFilterData(
    size: number = this.itemsPerPage, 
    page: number = this.currentPage,
    ) {
    return {
      params: {
        'page': page,
        'size': size,
        ...this.searchData
      }
    }
  }

  getOffers(url: string, params?) {
    this.loading = true;
    this.carService.getCars(url, params).subscribe(page => {
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
    this.currentPage = +event.pageIndex+1;
    this.itemsPerPage = +event.pageSize;
    this.getOffers(this.carService.baseLink, this.createFilterData());
    window.scroll(0,0);
  }

  changeSearch(form) {
    this.searchData = form;
    this.getOffers(this.carService.baseLink, this.createFilterData());
    this.paginator.firstPage();

  }




}
