import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ConfigurationService } from './configuration.service';
import { Observable } from 'rxjs';



export interface Page {
  count: number;
  next: string;
  previous: string;
  page: number;
  lastPage: number;
  size: number;
  results: Car[];
}

export interface Car {
  offerId: number;
  brand: string;
  model: string;
  production_year: number;
  mileage: number;
  primary_damage: string;
  secondary_damage: string;
  estimated_retail_value: number;
  vin: string;
  drive: string;
  body_style: string;
  vehicle_type: string;
  fuel: string;
  engine: string;
  transmission: string;
  color: string;
  location: string;
  sale_date: Date;
  sold: boolean;
  images: string[];
  current_price: number;
}

@Injectable({
  providedIn: 'root'
})
export class CarService {

  controlerUrl = "/cars"
  baseLink = `${this.controlerUrl}/list`;

  constructor(private http: HttpClient, private configuration: ConfigurationService) {}

  getCars(link: string, params?: {}): Observable<Page> {
    if (params) return this.http.get<Page>(`${this.configuration.apiUrl}${link}`, params);
    return this.http.get<Page>(`${this.configuration.apiUrl}${link}`);
  }

}
