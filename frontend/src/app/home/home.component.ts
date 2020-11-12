import { Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, NgForm } from '@angular/forms';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import { Observable, range } from 'rxjs';
import { filter, map, tap, toArray } from "rxjs/operators";
import { CarService, Page, Car } from "../services/car.service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  @ViewChild('paginator') paginator: MatPaginator;
  searchForm: FormGroup;

  cars: Car[];
  next: string;
  previous: string;

  length: number;
  itemsPerPage: number = 20;
  currentPage: number = 1;
  totalPages: number;

  constructor(private carService: CarService, private fb: FormBuilder) { }

  ngOnInit(): void {
    this.searchForm = this.fb.group({
      'brand': [''],
      'model': [''],
    })

    this.getOffers(this.carService.baseLink, this.createFilterData());
  }

  createFilterData(
    brand: string = this.searchForm.value['brand'],
    size: number = this.itemsPerPage, 
    page: number = this.currentPage,
    ) {
    return {
      params: {
        'page': page,
        'size': size,
        'brand': brand || '',
      }
    }
  }

  getOffers(url: string, params?) {
    this.carService.getCars(url, params).subscribe(page => {
      this.cars = page.results;
      this.length = page.count

      this.next = page.next;
      this.previous = page.previous;

      this.currentPage = page.page;
      this.totalPages = page.lastPage;

    });
  }

  pageChangeEvent(event: PageEvent) {
    this.currentPage = +event.pageIndex+1;
    this.itemsPerPage = +event.pageSize;
    this.getOffers(this.carService.baseLink, this.createFilterData());

    console.log(event);
  }

  onSubmit() {
    this.paginator.firstPage();
    this.currentPage = 1;
    this.getOffers(this.carService.baseLink, this.createFilterData());
  }

  resetForm() {
    this.searchForm.reset();
    this.getOffers(this.carService.baseLink, this.createFilterData());
  }


}
