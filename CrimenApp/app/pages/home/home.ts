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
  zones: Array<any>;
  types: Array<any>;
  selectedGraph: string;
  selectedZone: string;
  selectedType: string;
  messages: {};
  words: Array<any>;

  constructor(private menuCtrl: MenuController, private navController: NavController, private fb: FormBuilder, private API: APIService) {
    this.nav = navController;
    this.menu = menuCtrl;
    this.graphs = ["Concept Map", "Automatic Text Sizing", "Time Series Chart", "Heat Map"];
    this.zones = ["Todas", "Petare", "Valles del Tuy", "Catia", "Bello Monte"];
    this.types = ["Qué", "Cómo"];
    this.selectedGraph = "Automatic Text Sizing";
    this.selectedZone = "Todas";
    this.selectedType = "Qué";
    this.messages = {
      'automaticTextSizing': 'El tamaño de los círculos indica la popularidad del término en los eventos de crimen.',
      'heatMap': 'Los colores representan la popularidad del término en los eventos de crímenes a lo largo de los 7 días de la semana, mientras más oscuro el color más frecuente es el término.'
    }
    this.words = [];
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
    }  
  }

  destroyChart() {
    var svg = d3.select("svg").remove();
  }

  createConceptMap() {

  }

  contains(elem,list) {
    for (var i in list) {
      if (list[i] == elem) {
        return true;
      }
    }
    return false;
  }

  filterData(list) {
    var c = 1,
    j = 1,
    isAccepted = false,
    data = [],
    aux = [],
    filter = 0;
    
    if (this.selectedZone == "Todas") this.selectedType == "que" ? 50 : 20;

    this.words = [];
    for (var i in list) {
      if (j > 7) {
        return data;
      }
      var d = {
        "word": j,
        "day": list[i][1],
        "freq": list[i][2]
      };
      aux.push(d);
      if (filter <= list[i][2]) {
        isAccepted = true;
      }
      if (c == 7) {
        if ((isAccepted) && (!(this.contains(list[i][0],this.words)))) {
          this.words.push(list[i][0]);
          data = data.concat(aux);
          j += 1;
        }
        c = 0;
        isAccepted = false;
        aux = [];
      } else {
        c += 1; 
      }
    }
    return data;
  }

  createHeatMap() {
    this.loading = Loading.create({content:'Loading'});
    this.nav.present(this.loading);

    this.API.getHeatMapData(this.selectedZone)
      .subscribe(
        res => {
          this.loading.dismiss().then(()=>{
           
            var margin = { top: 30, right: 0, bottom: 100, left: 30 },
            width = 960 - margin.left - margin.right,
            height = 430 - margin.top - margin.bottom,
            gridSize = Math.floor(width / 24),
            legendElementWidth = 30,
            buckets = 9,
            colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"],
            days = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"],
            data = this.filterData(res[this.selectedType == "Qué" ? "que" : "como"]);

            var svg = d3.select("#chart").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            var wordLabels = svg.selectAll(".wordLabel")
                .data(this.words)
                .enter().append("text")
                  .text(function (d) { return d; })
                  .attr("x", 0)
                  .attr("y", function (d, i) { return i * gridSize; })
                  .style("text-anchor", "end")
                  .style("font-size", "10px")
                  .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
                  .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "wordLabel mono axis axis-workweek" : "wordLabel mono axis"); });

            var dayLabels = svg.selectAll(".dayLabel")
                .data(days)
                .enter().append("text")
                  .text(function(d) { return d; })
                  .attr("x", function(d, i) { return i * gridSize; })
                  .attr("y", 0)
                  .style("text-anchor", "middle")
                  .style("font-size", "10px")
                  .attr("transform", "translate(" + gridSize / 2 + ", -6)")
                  .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "dayLabel mono axis axis-worktime" : "dayLabel mono axis"); });

            var cards = svg.selectAll(".hour")
                .data(data, function(d) {return d.word+':'+d.day;});

            var colorScale = d3.scaleQuantile()
                .domain([0, buckets - 1, d3.max(data, function (d) { return d.freq; })])
                .range(colors);

            cards.enter()
              .append("rect")
                .attr("x", function(d) { return (d.day - 1) * gridSize; })
                .attr("y", function(d) { return (d.word - 1) * gridSize; })
                .attr("rx", 4)
                .attr("ry", 4)
                .attr("class", "hour bordered")
                .attr("width", gridSize)
                .attr("height", gridSize)
                .style("fill", colors[0])
                .transition().duration(1000)
                .style("fill", function(d) { return colorScale(d.freq); });

            cards.exit().remove();

            var legend = svg.selectAll(".legend")
                .data([0].concat(colorScale.quantiles()), function(d) { return d; })
                .enter()
                .append("g")
                  .attr("class", "legend")
                  .append("rect")
                    .attr("x", function(d, i) { return legendElementWidth * i; })
                    .attr("y", height)
                    .attr("width", legendElementWidth)
                    .attr("height", gridSize / 2)
                    .style("fill", function(d, i) { return colors[i]; });
            
            var legend = svg.selectAll(".legend")
                  .append("text")
                    .attr("class", "mono")
                    .text(function(d) { return "≥ " + Math.round(d); })
                    .attr("x", function(d, i) { return legendElementWidth * i; })
                    .attr("y", height + gridSize)
                    .style("font-size", "10px")
                    .exit().remove();

            this.presentToast(this.messages['heatMap']);
          }); 
        },
        error => {
          this.loading.dismiss().then(()=>{
            console.error(error);
          });
        }
      );
        
  }

  createAutomaticTextSizing() {
    this.loading = Loading.create({content:'Loading'});
    this.nav.present(this.loading);
    this.API.getTextSizeData(this.selectedZone)
      .subscribe(
        res => {
          this.loading.dismiss().then(()=>{
            var dataset = res;
            var diameter = 375;
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
                        return (d.data.type == "how" ? "#ff0202" : "#5998ff");
                    });

            node.append("text")
                    .attr("dy", ".3em")
                    .style("text-anchor", "middle")
                    .style("font-family", "Impact")
                    .text(function(d) {
                        return d.data.name.substring(0, d.r / 3);
                    })
                    .each(getSize)
                    .style("font-size", function(d) { return d.scale + "px"; });

            function getSize(d) {
              var bbox = this.getBBox(),
                  scale = bbox.width*0.2;
              d.scale = scale;
            }
            this.presentToast(this.messages['automaticTextSizing']);
          });
        },
        error => {
          this.loading.dismiss().then(()=>{
            console.error(error);
          });
        }
    );

  }

  createTimeSeriesChart() {
   
  }

}