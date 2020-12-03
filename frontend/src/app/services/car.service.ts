import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ConfigurationService } from './configuration.service';
import { Observable } from 'rxjs';
import {Page, Car, CarMap} from '../models/models';





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

  getCarById(id: number): Observable<Car> {
    return this.http.get<Car>(`${this.configuration.apiUrl}/cars/${id}`);
  }

  getAvailableFields(): Observable<CarMap> {
    return this.http.get<CarMap>(`${this.configuration.apiUrl}/cars/map`);
  }

  getAvailableModels(brand: string): Observable<string[]> {
    return this.http.get<string[]>(`${this.configuration.apiUrl}/cars/map/${brand}`);
  }

  getAvailableBrands(vType: string): Observable<string[]> {
    return this.http.get<string[]>(`${this.configuration.apiUrl}/cars/map/type/${vType}`);
  }

}
