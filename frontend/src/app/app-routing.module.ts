import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { OfferDetailsComponent } from './offer/offer-details/offer-details.component';
import { OfferComponent } from './offer/offer.component';



const routes: Routes = [
  {
    path: '', component: HomeComponent, data: {
      shouldReuse: true,
      reuseRoutesFrom: ['offers']
    }
  },
  {
    path: 'offers', component: OfferComponent, data: {
      shouldReuse: true,
      reuseRoutesFrom: ['offer/:id']

    }
  },
  { path: 'offer/:id', component: OfferDetailsComponent },

  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    anchorScrolling: 'enabled'
  })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
