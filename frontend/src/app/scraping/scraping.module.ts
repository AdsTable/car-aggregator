import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ScrapingRoutingModule } from './scraping-routing.module';
import { ScrapingComponent } from './scraping.component';
import {MatTableModule} from '@angular/material/table';
import {FlexLayoutModule} from "@angular/flex-layout";
import {MatTabsModule} from '@angular/material/tabs';
import { JobsComponent } from './jobs/jobs.component';
import {MatIconModule} from "@angular/material/icon";
import {MatButtonModule} from "@angular/material/button";
import {MatMenuModule} from "@angular/material/menu";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";



@NgModule({
  declarations: [ScrapingComponent, JobsComponent],
  imports: [
    CommonModule,
    ScrapingRoutingModule,
    MatTableModule,
    FlexLayoutModule,
    MatTabsModule,
    MatIconModule,
    MatButtonModule,
    MatMenuModule,


  ]
})
export class ScrapingModule { }
