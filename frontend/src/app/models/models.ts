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
    estimated_repair_cost: number;
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
    thumb_image: string;
    current_price: number;
    auction_site: string;
    loss_type: string;
    buy_now: string;
  }
  
  
  export interface CarMap {
    brand: string[];
    fuel: string[];
    primary_damage: string[];
    body_style: string[];
    transmission: string[];
    drive: string[];
    production_year: number[];
    vehicle_type: string[];
  }