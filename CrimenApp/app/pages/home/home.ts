import {Component} from '@angular/core';
import {NavController, MenuController, Loading, Alert, Toast} from 'ionic-angular';
import {FORM_DIRECTIVES, FormBuilder,  ControlGroup, Validators, AbstractControl} from '@angular/common';
import {APIService} from '../../providers/API.service';

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
  messages: {};

  constructor(private menuCtrl: MenuController, private navController: NavController, private fb: FormBuilder, private API: APIService) {
    this.nav = navController;
    this.menu = menuCtrl;
    this.graphs = ["Concept Map", "Automatic Text Sizing", "Time Series Chart", "Heat Map"];
    this.selectedGraph = "Pie Chart";
    this.messages = {
      'automaticTextSizing': 'El tamaño de los círculos indica la popularidad del término en los eventos de crimen.'
    }
  }

  presentToast(message) {  
    let toast = Toast.create({
      message: message,
      showCloseButton: true,
      position: 'bottom'
    });

    this.nav.present(toast);
  }

  drawChart() {
    switch (this.selectedGraph) {  
      case "Concept Map":
        this.destroyChart();
        this.createConceptMap();
        break;  
      case "Automatic Text Sizing":
        this.destroyChart(); 
        this.createAutomaticTextSizing();
        break;  
      case "Time Series Chart":
        this.destroyChart();  
        this.createTimeSeriesChart();
        break;
       case "Heat Map":
        this.destroyChart();  
        this.createHeatMap();
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

  createHeatMap() {
    var margin = { top: 50, right: 0, bottom: 100, left: 30 },
        width = 960 - margin.left - margin.right,
        height = 430 - margin.top - margin.bottom,
        gridSize = Math.floor(width / 24),
        legendElementWidth = gridSize*2,
        buckets = 9,
        colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"], // alternatively colorbrewer.YlGnBu[9]
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
        times = ["1a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a", "12a", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p", "10p", "11p", "12p"],
        datasets = ["data.tsv", "data2.tsv"];

    var svg = d3.select("#chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var dayLabels = svg.selectAll(".dayLabel")
        .data(days)
        .enter().append("text")
          .text(function (d) { return d; })
          .attr("x", 0)
          .attr("y", function (d, i) { return i * gridSize; })
          .style("text-anchor", "end")
          .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
          .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

    var timeLabels = svg.selectAll(".timeLabel")
        .data(times)
        .enter().append("text")
          .text(function(d) { return d; })
          .attr("x", function(d, i) { return i * gridSize; })
          .attr("y", 0)
          .style("text-anchor", "middle")
          .attr("transform", "translate(" + gridSize / 2 + ", -6)")
          .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

    var heatmapChart = function(tsvFile) {
      d3.tsv(tsvFile,
      function(d) {
        return {
          day: +d.day,
          hour: +d.hour,
          value: +d.value
        };
      },
      function(error, data) {
        var colorScale = d3.scale.quantile()
            .domain([0, buckets - 1, d3.max(data, function (d) { return d.value; })])
            .range(colors);

        var cards = svg.selectAll(".hour")
            .data(data, function(d) {return d.day+':'+d.hour;});

        cards.append("title");

        cards.enter().append("rect")
            .attr("x", function(d) { return (d.hour - 1) * gridSize; })
            .attr("y", function(d) { return (d.day - 1) * gridSize; })
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("class", "hour bordered")
            .attr("width", gridSize)
            .attr("height", gridSize)
            .style("fill", colors[0]);

        cards.transition().duration(1000)
            .style("fill", function(d) { return colorScale(d.value); });

        cards.select("title").text(function(d) { return d.value; });
        
        cards.exit().remove();

        var legend = svg.selectAll(".legend")
            .data([0].concat(colorScale.quantiles()), function(d) { return d; });

        legend.enter().append("g")
            .attr("class", "legend");

        legend.append("rect")
          .attr("x", function(d, i) { return legendElementWidth * i; })
          .attr("y", height)
          .attr("width", legendElementWidth)
          .attr("height", gridSize / 2)
          .style("fill", function(d, i) { return colors[i]; });

        legend.append("text")
          .attr("class", "mono")
          .text(function(d) { return "≥ " + Math.round(d); })
          .attr("x", function(d, i) { return legendElementWidth * i; })
          .attr("y", height + gridSize);

        legend.exit().remove();

      });  
    };

    heatmapChart(datasets[0]);
    
    var datasetpicker = d3.select("#dataset-picker").selectAll(".dataset-button")
      .data(datasets);

    datasetpicker.enter()
      .append("input")
      .attr("value", function(d){ return "Dataset " + d })
      .attr("type", "button")
      .attr("class", "dataset-button")
      .on("click", function(d) {
        heatmapChart(d);
      });

  }

  createAutomaticTextSizing() {
    this.loading = Loading.create({content:'Loading'});
    this.nav.present(this.loading);
    this.API.getTextSize()
      .subscribe(
        res => {
          this.loading.dismiss().then(()=>{
            var dataset = res;
            var diameter = 375;
            var color = d3.scaleOrdinal(d3.schemeCategory20);
            var bubble = d3.pack(dataset)
                    .size([diameter, diameter])
                    .padding(1.5);
            var svg = d3.select("#chart")
                    .append("svg")
                    .attr("width", diameter)
                    .attr("height", diameter + 100)
                    .attr("class", "bubble");

            var nodes = d3.hierarchy(dataset)
                    .sum(function(d) { return d.freq; });

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
                        return d.data.name + ": " + d.data.freq;
                    });

            node.append("circle")
                    .attr("r", function(d) {
                        return d.r;
                    })
                    .style("fill", function(d) {
                        return color(d.name);
                    });

            node.append("text")
                    .attr("dy", ".3em")
                    .style("text-anchor", "middle")
                    .text(function(d) {
                        return d.data.name.substring(0, d.r / 3) + ": " + d.data.freq;
                    })
                    .each(getSize)
                    .style("font-size", function(d) { return d.scale + "px"; });

            function getSize(d) {
              var bbox = this.getBBox(),
                  scale = bbox.width*0.1;
              d.scale = scale;
            }

            this.presentToast(this.messages['automaticTextSizing']);
          });
        },
        error => {
          console.error(error);
        }
    );

  }


  createTimeSeriesChart() {
   
  }

  // Pruebas con la libreria svg.
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