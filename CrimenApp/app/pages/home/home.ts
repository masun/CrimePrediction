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
  graphs: Array<any>;
  selectedGraph: string;

  constructor(private menuCtrl: MenuController, private navController: NavController, private fb: FormBuilder) {
    this.nav = navController;
    this.menu = menuCtrl;
    this.loading = Loading.create({content:'Loading'});
    this.graphs = ["Concept Map", "Automatic Text Sizing", "Time Series Chart"];
    this.selectedGraph = "Pie Chart";
  }

  drawChart() {
    switch (this.selectedGraph) {  
      case "Concept Map":
        this.destroyChart();
        // this.createConceptMap();
        this.createPieChart();  
        break;  
      case "Automatic Text Sizing":
        this.destroyChart(); 
        this.createAutomaticTextSizing();
        // this.createPieChart();  
        break;  
      case "Time Series Chart":
        this.destroyChart();  
        this.createTimeSeriesChart();
        // this.createPieChart();
        break; 
      default:
        this.destroyChart();  
        this.createPieChart();  
    }  
  }

  destroyChart() {
    var svg = d3.select("svg").remove();
  }

  createConceptMap() {

  }

  createAutomaticTextSizing() {
    var dataset = {
        "children": [{
            "facilityId": "FAC0001",
            "responseCount": 2
        }, {
            "facilityId": "FAC0006",
            "responseCount": 2
        }, {
            "facilityId": "FAC0002",
            "responseCount": 1
        }, {
            "facilityId": "FAC0003",
            "responseCount": 2
        }, {
            "facilityId": "FAC0004",
            "responseCount": 3
        }, {
            "facilityId": "FAC0005",
            "responseCount": 1
        }]
    };

    var diameter = 300;
    var color = d3.scaleOrdinal(d3.schemeCategory20);


    var bubble = d3.pack(dataset)
            .size([diameter, diameter])
            .padding(1.5);
    var svg = d3.select("#chart")
            .append("svg")
            .attr("width", diameter)
            .attr("height", diameter)
            .attr("class", "bubble");

    var nodes = d3.hierarchy(dataset)
            .sum(function(d) { return d.responseCount; });

    var node = svg.selectAll(".node")
            .data(bubble(nodes).descendants())
            .enter()
            .filter(function(d){
                return  !d.children
            })
            .append("g")
            .attr("class", "node")
            .attr("transform", function(d) {
                return "translate(" + d.x + "," + d.y + ")";
            });

    node.append("title")
            .text(function(d) {
                return d.facilityId + ": " + d.responseCount;
            });

    node.append("circle")
            .attr("r", function(d) {
                return d.r;
            })
            .style("fill", function(d) {
                return color(d.facilityId);
            });

    node.append("text")
            .attr("dy", ".3em")
            .style("text-anchor", "middle")
            .text(function(d) {
                return d.data.facilityId.substring(0, d.r / 3) + ": " + d.data.responseCount;
            });


  }


  createTimeSeriesChart() {
   
  }

  createPieChart() {
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