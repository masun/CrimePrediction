import {Component} from '@angular/core';
import {NavController, MenuController, Loading, Alert} from 'ionic-angular';
import {FORM_DIRECTIVES, FormBuilder,  ControlGroup, Validators, AbstractControl} from '@angular/common';
declare var d3: any;

@Component({
  templateUrl: 'build/pages/home/home.html',
  directives: [FORM_DIRECTIVES]
})

export class Home {
  nav: NavController;
  menu: MenuController;
  loading: Loading;
  alert: Alert;
  draw: boolean;

  constructor(private menuCtrl: MenuController, private navController: NavController, private fb: FormBuilder) {
    this.nav = navController;
    this.menu = menuCtrl;
    this.loading = Loading.create({content:'Loading'});
    this.draw = true;
  }

  drawChart() {
    if (this.draw) {
      this.createChart();
      this.draw = false;
    } else {
      this.destroyChart();
      this.draw = true;
    }
  }

  destroyChart() {
    var svg = d3.select("svg").remove();
  }

  createChart() {
    var dataset = [
      { label: 'Abulia', count: 10 },
      { label: 'Betelgeuse', count: 20 },
      { label: 'Cantaloupe', count: 30 },
      { label: 'Dijkstra', count: 40 }
    ];
    var width = 360;
    var height = 360;
    var radius = Math.min(width, height) / 2;
    var color = d3.scaleOrdinal(d3.schemeCategory20b);
    var svg = d3.select('#chart')
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', 'translate(' + (width / 2) +  ',' + (height / 2) + ')');
    var arc = d3.arc()
      .innerRadius(0)
      .outerRadius(radius);
    var pie = d3.pie()
      .value(function(d) { return d.count; })
      .sort(null);
    var path = svg.selectAll('path')
      .data(pie(dataset))
      .enter()
      .append('path')
      .attr('d', arc)
      .attr('fill', function(d, i) {
        return color(d.data.label);
      });
  }
  
}