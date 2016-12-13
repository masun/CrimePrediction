import {Injectable} from '@angular/core';
import {Component} from '@angular/core';
import {NavController, Platform} from 'ionic-angular';
import {Http, Response, Headers,  URLSearchParams} from '@angular/http';
import {Observable} from 'rxjs/Observable';

import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';

@Injectable()
export class APIService {
    serverURL: string;
    authCredentials: {};

    constructor(private http:Http, private platform: Platform) {
        this.platform = platform;
        this.serverURL = 'http://127.0.0.1:8000';

        this.authCredentials = {};
    }

    createUser(username, password) {
        var service = '/usuarios/';
        var authCredentials = {
            'email': username,
            'password': password
        };

        var headers:any = new Headers();
            headers.append('Content-Type', 'application/json');
        return this.http.post(this.serverURL+service, JSON.stringify(authCredentials), {headers: headers})
                        .map((res:Response) => res.json())
                        .catch(this.handleError);

    }

    loginUser(username, password) {
        var service = '/usuarios/login';
        var authCredentials = {
            'email': username,
            'password': password
        };

        var headers:any = new Headers();
            headers.append('Content-Type', 'application/json');
        return this.http.post(this.serverURL+service, JSON.stringify(authCredentials), {headers: headers})
                        .map((res:Response) => res.json())
                        .catch(this.handleError);

    }

    getTextSizeData(selectedZone){
        var service = '/tweets/textSize';

        var headers:any = new Headers();
            headers.append('Content-Type', 'application/json');
        if (selectedZone == "Todas") {
            return this.http.get(this.serverURL+service, {headers: headers})
                            .map((res:Response) => res.json())
                            .catch(this.handleError);
        } else {
            var body = {
                "zona": selectedZone
            };
            return this.http.post(this.serverURL+service, JSON.stringify(body), {headers: headers})
                            .map((res:Response) => res.json())
                            .catch(this.handleError);
        }
    }

    getHeatMapData(selectedZone){
        var service = '/tweets/heatMap';

        var headers:any = new Headers();
            headers.append('Content-Type', 'application/json');
        if (selectedZone == "Todas") {
            return this.http.get(this.serverURL+service, {headers: headers})
                            .map((res:Response) => res.json())
                            .catch(this.handleError);
        } else {
            var body = {
                "zona": selectedZone
            };
            return this.http.post(this.serverURL+service, JSON.stringify(body), {headers: headers})
                            .map((res:Response) => res.json())
                            .catch(this.handleError);
        }
    }


    getHeader(){
        var headers:any = new Headers();
        headers.append('Content-Type', 'application/json');
           headers.append('token', this.authCredentials['token']);

        return headers;
    }

    private handleError (error: Response) {
        console.log(error);
        return Observable.throw(error.json().msg || 'Server error');
      }

}