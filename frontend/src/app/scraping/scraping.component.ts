import { Component, OnInit } from '@angular/core';
import {ScrapingService} from "../services/scraping.service";
import {interval, Observable, Subscription, timer} from "rxjs";
import {ScrapyState} from "../models/models";
import {switchMap} from "rxjs/operators";

@Component({
  selector: 'app-scraping',
  templateUrl: './scraping.component.html',
  styleUrls: ['./scraping.component.scss']
})
export class ScrapingComponent implements OnInit {

  spider: Subscription;
  state$: Observable<ScrapyState>
  spiders$: Observable<string[]>

  constructor(private service: ScrapingService) { }

  ngOnInit(): void {
    this.state$ = timer(0,10000).pipe(
            switchMap(() => this.service.getJobs()),
        );

    this.spiders$ = this.service.getSpiders();
  }

  runSpider(spider: string) {
    this.spider = this.service.runSpider(spider).subscribe((data) => {
      console.log(data);
    })
  }

  ngOnDestroy() {
    this.spider.unsubscribe();
  }
}
