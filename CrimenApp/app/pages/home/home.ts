import {Component} from '@angular/core';
import {NavController, MenuController, Loading, Alert} from 'ionic-angular';
import {FORM_DIRECTIVES, FormBuilder,  ControlGroup, Validators, AbstractControl} from '@angular/common';

@Component({
  templateUrl: 'build/pages/home/home.html',
  directives: [FORM_DIRECTIVES]
})

export class Home {

  nav: NavController;
  menu: MenuController;
  loading: Loading;
  alert: Alert;

  constructor(private menuCtrl: MenuController, private navController: NavController, private fb: FormBuilder) {
    this.nav = navController;
    this.menu = menuCtrl;
    this.loading = Loading.create({content:'Loading'});
  }
  
}