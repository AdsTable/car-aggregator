import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { OfferDetailsComponent } from './offer/offer-details/offer-details.component';
import { OfferComponent } from './offer/offer.component';
import { LimitedGuard } from './shared/guards';



const routes: Routes = [
  {
    path: 'home', component: HomeComponent
  },
  {
    path: 'offers', component: OfferComponent, data: {
      shouldReuse: true,
      reuseRoutesFrom: ['offer/:id']
    }, canActivate: [LimitedGuard]
  },
  { path: 'offer/:id', component: OfferDetailsComponent },
  { path: 'scraping', loadChildren: () => import('./scraping/scraping.module').then(m => m.ScrapingModule) },

  { path: '**', redirectTo: 'home' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    anchorScrolling: 'enabled'
  })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
