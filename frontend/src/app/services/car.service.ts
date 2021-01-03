import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ConfigurationService } from './configuration.service';
import { Observable } from 'rxjs';
import {Page, Car, CarMap} from '../models/models';





@Injectable({
  providedIn: 'root'
})
export class CarService {

  controllerUrl = "/cars"
  baseLink = `${this.controllerUrl}/list`;

  constructor(private http: HttpClient, private configuration: ConfigurationService) {}

  getCars(link: string, params?: {}): Observable<Page> {
    if (params) return this.http.get<Page>(`${this.configuration.apiUrl}${link}`, params);
    return this.http.get<Page>(`${this.configuration.apiUrl}${link}`);
  }

  getCarById(id: number): Observable<Car> {
    return this.http.get<Car>(`${this.configuration.apiUrl}/cars/${id}`);
  }

  getAvailableFields(): Observable<CarMap> {
    return this.http.get<CarMap>(`${this.configuration.apiUrl}/cars/map`);
  }
  //
  // getAvailableModels(brand: string): Observable<string[]> {
  //   return this.http.get<string[]>(`${this.configuration.apiUrl}/cars/models/${brand}`);
  // }

  getAvailableModels(type?: string, brand?: string): Observable<string[]> {
    return this.http.get<string[]>(`${this.configuration.apiUrl}/cars/models/?type=${type}&brand=${brand}`)
  }

  getAvailableBrands(vType: string): Observable<string[]> {
    return this.http.get<string[]>(`${this.configuration.apiUrl}/cars/map/type/${vType}`);
  }

  getSimiliarById(id: number): Observable<Car[]> {
    return this.http.get<Car[]>(`${this.configuration.apiUrl}/cars/similiar/${id}`);
  }

  postEmail(data: any) {
    return this.http.post<Car>(`${this.configuration.apiUrl}/cars/sendform`, data);
  }

}
