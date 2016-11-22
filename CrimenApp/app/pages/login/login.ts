import {Component} from '@angular/core';
import {NavController, MenuController, Loading, Alert} from 'ionic-angular';
import {FORM_DIRECTIVES, FormBuilder,  ControlGroup, Validators, AbstractControl} from '@angular/common';
import {Home} from '../home/home';

@Component({
  templateUrl: 'build/pages/login/login.html',
  directives: [FORM_DIRECTIVES]
})

export class Login {

  authForm: ControlGroup;
  username: AbstractControl;
  password: AbstractControl;
  nav: NavController;
  menu: MenuController;
  loading: Loading;
  alert: Alert;

  constructor(private menuCtrl: MenuController, private navController: NavController, private fb: FormBuilder) {
    this.authForm = fb.group({  
      'username': ['', Validators.compose([Validators.required])],
      'password': ['', Validators.compose([Validators.required])]
    });

    this.username = this.authForm.controls['username'];     
    this.password = this.authForm.controls['password'];
    this.nav = navController;
    this.menu = menuCtrl;
    this.loading = Loading.create({content:'Loading'});
    this.alert = Alert.create({
      title: 'Authentication error!',
      subTitle: 'Wrong username or password',
      buttons: ['OK']
    });
  }

  onSubmit(value) { 
    console.log("VALUE: ", value);
    if (this.authForm.valid) {
      // this.nav.present(this.loading);
      console.log("USERANEM: ", value['username']);
      console.log("PASSWORD: ", value['password']);
      this.nav.setRoot(Home);
      // if (value['username'] == "123" && value['password'] == "123") {
      //   this.nav.push(Home);
      // }
    }
  }
}
