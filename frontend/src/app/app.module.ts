import { BrowserModule } from '@angular/platform-browser';
import { DEFAULT_CURRENCY_CODE, LOCALE_ID, NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatSliderModule } from "@angular/material/slider";
import { MatPaginatorModule } from "@angular/material/paginator";
import { HomeComponent } from './home/home.component';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { SearchComponent } from './search/search.component';
import { MatCardModule } from '@angular/material/card';
import { FlexLayoutModule } from '@angular/flex-layout';
import { RouteReuseStrategy } from '@angular/router';
import { CustomReuseStrategy } from './shared/custom-resuse-strategy';
import { MatCarouselModule } from '@ngbmodule/material-carousel';
import { registerLocaleData } from '@angular/common';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatIconModule} from '@angular/material/icon';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatToolbarModule} from '@angular/material/toolbar'
import { MatListModule } from '@angular/material/list';
import {LimitedGuard} from './shared/guards';
import localePl from '@angular/common/locales/pl';
import localeEnUS from '@angular/common/locales/en';
import { ReversePipe } from './shared/reverse.pipe';
import { OfferComponent } from './offer/offer.component';
import { OfferDetailsComponent } from './offer/offer-details/offer-details.component';
import { OfferFilterComponent } from './offer/offer-filter/offer-filter.component';


registerLocaleData(localePl, 'pl');
registerLocaleData(localeEnUS, 'en');


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    SearchComponent,
    ReversePipe,
    OfferComponent,
    OfferDetailsComponent,
    OfferFilterComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatSliderModule,
    HttpClientModule,
    ReactiveFormsModule,

    MatPaginatorModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    MatSelectModule,
    MatAutocompleteModule,
    MatProgressSpinnerModule,
    MatProgressBarModule,
    MatExpansionModule,
    MatIconModule,
    MatSidenavModule,
    MatListModule,
    MatToolbarModule,

    FlexLayoutModule,
    MatCarouselModule.forRoot(),
  ],
  providers: [
    {provide: RouteReuseStrategy, useClass: CustomReuseStrategy},
    { provide: LOCALE_ID, useValue: "pl" },
    LimitedGuard
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
