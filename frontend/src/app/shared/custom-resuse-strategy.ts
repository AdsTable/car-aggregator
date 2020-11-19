import { ActivatedRouteSnapshot, DetachedRouteHandle, RouteReuseStrategy } from '@angular/router';


export class CustomReuseStrategy implements RouteReuseStrategy {
    handlers: {[key: string]: DetachedRouteHandle} = {}
    private routeLeftFrom: string;

    shouldDetach(route: ActivatedRouteSnapshot): boolean {
        // console.debug('CustomReuseStrategy:shouldDetach', route);
        this.routeLeftFrom = route.routeConfig.path;
        return route.data.shouldReuse || false;
    }

    store(route: ActivatedRouteSnapshot, handle: {}): void {
        // console.debug('CustomReuseStrategy:store', route, handle);
        if (route.data.shouldReuse) {
            this.handlers[route.routeConfig.path] = handle;
        }
    }

    shouldAttach(route: ActivatedRouteSnapshot): boolean {
        let wasRoutePreviouslyDetached = !!this.handlers[route.url.join('/') || route.parent.url.join('/')];
        if (wasRoutePreviouslyDetached) {
            let reuseRouteFromVerified = route.data.reuseRoutesFrom?.indexOf(this.routeLeftFrom) > -1;

            if (reuseRouteFromVerified) {
                return true;
            }
        }
        return false;
        // console.debug('CustomReuseStrategy:shouldAttach', route);
        // return !!route.routeConfig && !!this.handlers[route.routeConfig.path];
    }

    retrieve(route: ActivatedRouteSnapshot): DetachedRouteHandle {
        // console.debug('CustomReuseStrategy:retrieve', route);
        if (!route.routeConfig) return null;
        return this.handlers[route.routeConfig.path];
    }

    shouldReuseRoute(future: ActivatedRouteSnapshot, curr: ActivatedRouteSnapshot): boolean {
        // console.debug('CustomReuseStrategy:shouldReuseRoute', future, curr);
        return future.data.shouldReuse || false;
    }
}