import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ScrapingComponent } from './scraping.component';

const routes: Routes = [{ path: '', component: ScrapingComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ScrapingRoutingModule { }
