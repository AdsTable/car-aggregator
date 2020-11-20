import { ActivatedRouteSnapshot, DetachedRouteHandle, RouteReuseStrategy } from '@angular/router';


export class CustomReuseStrategy implements RouteReuseStrategy {
    handlers: { [key: string]: DetachedRouteHandle } = {}
    private routeLeftFrom: string;

    shouldDetach(route: ActivatedRouteSnapshot): boolean {
        this.routeLeftFrom = route.routeConfig.path;
        return route.data.shouldReuse || false;
    }

    store(route: ActivatedRouteSnapshot, handle: {}): void {
        if (route.data.shouldReuse) {
            this.handlers[route.routeConfig.path] = handle;
        }
    }

    shouldAttach(route: ActivatedRouteSnapshot): boolean {
        let wasRoutePreviouslyDetached = !!this.handlers[route.url.join('/')];
        if (wasRoutePreviouslyDetached) {
            let reuseRouteFromVerified = route.data.reuseRoutesFrom?.indexOf(this.routeLeftFrom) > -1;

            if (reuseRouteFromVerified) {
                return true;
            }
        }
        return false;
    }

    retrieve(route: ActivatedRouteSnapshot): DetachedRouteHandle {
        if (!route.routeConfig) return null;
        return this.handlers[route.routeConfig.path];
    }

    shouldReuseRoute(future: ActivatedRouteSnapshot, curr: ActivatedRouteSnapshot): boolean {
        let reUseUrl = false;
        if(future.routeConfig) {
            if(future.routeConfig.data) {
                reUseUrl = future.routeConfig.data.shouldReuse;
            }
        }

        const defaultReuse = (future.routeConfig === curr.routeConfig);

        return reUseUrl || defaultReuse;
    }
}

