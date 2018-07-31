var hiData = {};

d3.queue()
    // .defer(d3.csv, "../../winereviews/word_count_stats_rating_hi/500")
    .defer(d3.csv, "../../static/data/word_count_stats_rating_hi.csv")
    .await(analyzeHi);

function analyzeHi(error, words) {
    if(error) { console.log(error); }
    hiData = words;
    initializeWordCountHi(initNum);
}

// set the dimensions and margins of the graph
var marginSvgHi = {top: 30, right: 20, bottom: 80, left: 40},
    width = barChartWidth - marginSvgHi.left - marginSvgHi.right,
    height = barChartHeight - marginSvgHi.top - marginSvgHi.bottom;

// set the ranges
var xSvgHi = d3.scaleBand()
          .range([0, width])
          .padding(0.1);
var ySvgHi = d3.scaleLinear()
          .range([height, 0]);
          
// append the svg object to the body of the page
// append a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svgHi = d3.select("div#bar_hi").append("svg")
    .attr("id", "word_count_stats_hi")
    .attr("width", width + marginSvgHi.left + marginSvgHi.right)
    .attr("height", height + marginSvgHi.top + marginSvgHi.bottom)
  .append("g")
    .attr("transform", 
          "translate(" + marginSvgHi.left + "," + marginSvgHi.top + ")");


function initializeWordCountHi (number) { 
    
    var barColor = "rgb(156, 158, 222)";
    //rgb(214, 97, 107)
    var chartTitle = "Top "+(number)+" Words Used in the 100 Highest Rated Wines";
    var data = hiData.slice(0, number);
    data = data.reverse();
    d3.selectAll("#word_count_stats_hi > g > *").remove();

    // format the data
    data.forEach(function(d) {
        d.value = +d.value;
    });
    
    // Scale the range of the data in the domains
    xSvgHi.domain(data.map(function(d) { return d.id; }));
    ySvgHi.domain([0, d3.max(data, function(d) { return d.value; })]);
    
    // append the rectangles for the bar chart
    svgHi.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", function(d){ return "bar searchFunction " + d.id; })
        .attr("x", function(d) { return xSvgHi(d.id); })
        .attr("width", xSvgHi.bandwidth())
        .attr("y", function(d) { return ySvgHi(d.value); })
        .attr("height", function(d) { return height - ySvgHi(d.value); })
        .attr("opacity", opacityStart)
        .attr("fill", barColor)
        .on("mouseover", function(d) {
            
            d3.selectAll("."+d.id)
                .attr("opacity", opacityRollover);

            tooltip.text(d.id + ": Avg Rating " + format(d.avg_rating));
            tooltip.style("visibility", "visible");
        })
        .on("mousemove", function() {
            return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
        })
        .on("mouseout", function(d){
            
            d3.selectAll("."+d.id)
                .attr("opacity", opacityStart);
                
            return tooltip.style("visibility", "hidden");
            
        })
        .on("click", function(d){
        });
;
    
    // add the x Axis
    svgHi.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xSvgHi))
        .selectAll("text")
        .attr("y", 0)
        .attr("x", 9)
        .attr("dy", ".35em")
        .attr("transform", "rotate(90)")
        .attr("fill", chartText)
        .style("text-anchor", "start");
    

    // add the y Axis
    svgHi.append("g")
        .call(d3.axisLeft(ySvgHi))
        .selectAll("text")
        .attr("fill", chartText)
        ;
        
    // text label for the x axis
    svgHi.append("text")             
        .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + marginSvgHi.top + marginSvgHi.bottom/2) + ")")
        .style("text-anchor", "middle")
        .text("Word")
        .attr("fill", chartText);

    // text label for the y axis
    svgHi.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y",0 - marginSvgHi.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Count")
        .attr("fill", chartText); 
        
    // TITLE text label
    svgHi.append("text")
        .attr("transform",
            "translate(" + (width/2) + " , -10)")
        .style("text-anchor", "middle")
        .text(chartTitle)
        .attr("class", "chartTitle")
        .attr("fill", chartText);
        
    svgHi.append("g")
        .attr("transform",
            "translate(20 , 20)")
        .attr("class", "top5")
        .append("text")
        .text("Top 5:")
        .attr("class","top5heading")
        .attr("fill", chartText);
        ;


    var top5data = hiData.slice(0, 5);
    
    for (var i = 0; i < top5data.length; i++) {
        console.log(top5data[i]);
        svgHi.select(".top5")
            .append("text")
            .text(top5data[i].id)
            .attr("dy", (1.2+i*1.2)+"em")
            .attr("fill", chartText);
    }

}