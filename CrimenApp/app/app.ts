import {Component, ViewChild} from '@angular/core';
import {Platform, ionicBootstrap, MenuController, Nav} from 'ionic-angular';
import {StatusBar} from 'ionic-native';
import {MovieListPage} from './pages/movie-list/movie-list';
import {Login} from './pages/login/login';
import {Home} from './pages/home/home';

@Component({
  templateUrl: 'build/app.html',
})

export class MyApp {
  @ViewChild(Nav) nav: Nav;

  rootPage: any = Login;
  pages: any[];

  constructor(private platform: Platform, public menu: MenuController) {
    this.menu = menu;
    this.pages = [
      { title: 'Home', component: Home }
    ];
    platform.ready().then(() => {
      // Okay, so the platform is ready and our plugins are available.
      // Here you can do any higher level native things you might need.
      StatusBar.styleDefault();
    });
  }

  openPage(page) {
    // close the menu when clicking a link from the menu
    this.menu.close();
    // navigate to the new page if it is not the current page
    this.nav.setRoot(page.component);
  }
}

ionicBootstrap(MyApp);
