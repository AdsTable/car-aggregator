import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {ConfigurationService} from "./configuration.service";
import {Observable} from "rxjs";
import {ScrapyState, Job} from '../models/models';


@Injectable({
  providedIn: 'root'
})
export class ScrapingService {

  constructor(private http: HttpClient, private configuration: ConfigurationService) { }

  public getJobs(): Observable<ScrapyState> {
    return this.http.get<ScrapyState>(`${this.configuration.apiUrl}/cars/scraper/jobs`);
  }

  public getSpiders(): Observable<string[]> {
    return this.http.get<string[]>(`${this.configuration.apiUrl}/cars/scraper/spiders`);
  }

  public runSpider(spider: string) {
    return this.http.get(`${this.configuration.apiUrl}/cars/scraper/start/${spider}`);
  }

  public cancelJob(jobId: string) {
    return this.http.get(`${this.configuration.apiUrl}/cars/scraper/job/${jobId}/cancel`);
  }
}
