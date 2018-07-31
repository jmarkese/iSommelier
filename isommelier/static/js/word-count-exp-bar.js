var expData = {};

d3.queue()
    // .defer(d3.csv, "../../winereviews/word_count_stats_rating_hi/500")
    .defer(d3.csv, "../../static/data/word_count_stats_expensive.csv")
    .await(analyzeExp);

function analyzeExp(error, words) {
    if(error) { console.log(error); }
    expData = words;
    initializeWordCountExp(initNum);
}

// set the dimensions and margins of the graph
var marginSvgExp = {top: 30, right: 20, bottom: 80, left: 40},
    width = barChartWidth - marginSvgExp.left - marginSvgExp.right,
    height = barChartHeight - marginSvgExp.top - marginSvgExp.bottom;

// set the ranges
var xSvgExp = d3.scaleBand()
          .range([0, width])
          .padding(0.1);
var ySvgExp = d3.scaleLinear()
          .range([height, 0]);
          
// append the svg object to the body of the page
// append a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svgExp = d3.select("div#bar_exp").append("svg")
    .attr("id", "word_count_stats_expensive")
    .attr("width", width + marginSvgExp.left + marginSvgExp.right)
    .attr("height", height + marginSvgExp.top + marginSvgExp.bottom)
  .append("g")
    .attr("transform", 
          "translate(" + marginSvgExp.left + "," + marginSvgExp.top + ")");


function initializeWordCountExp (number) { 
    
    var barColor = "rgb(99, 121, 57)";
    var chartTitle = "Top "+(number)+" Words Used in the 100 Most Expensive Wines";
    var data = expData.slice(0, number);
    data = data.reverse();
    d3.selectAll("#word_count_stats_expensive > g > *").remove();

    // format the data
    data.forEach(function(d) {
        d.value = +d.value;
    });
    
    // Scale the range of the data in the domains
    xSvgExp.domain(data.map(function(d) { return d.id; }));
    ySvgExp.domain([0, d3.max(data, function(d) { return d.value; })]);
    
    // append the rectangles for the bar chart
    svgExp.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", function(d){ return "bar searchFunction " + d.id; })
        .attr("x", function(d) { return xSvgExp(d.id); })
        .attr("width", xSvgExp.bandwidth())
        .attr("y", function(d) { return ySvgExp(d.value); })
        .attr("height", function(d) { return height - ySvgExp(d.value); })
        .attr("opacity", opacityStart)
        .attr("fill", barColor)
        .on("mouseover", function(d) {
            
            d3.selectAll("."+d.id)
                .attr("opacity", opacityRollover);

            tooltip.text(d.id + ": Avg Price $" + format(d.avg_price));
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

    // add the x Axis
    svgExp.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xSvgExp))
        .selectAll("text")
        .attr("y", 0)
        .attr("x", 9)
        .attr("dy", ".35em")
        .attr("transform", "rotate(90)")
        .attr("fill", chartText)
        .style("text-anchor", "start");
    

    // add the y Axis
    svgExp.append("g")
        .call(d3.axisLeft(ySvgExp))
        .selectAll("text")
        .attr("fill", chartText)
        ;
        
    // text label for the x axis
    svgExp.append("text")             
        .attr("transform",
            "translate(" + (width/2) + " ," + 
                           (height + marginSvgExp.top + marginSvgExp.bottom/2) + ")")
        .style("text-anchor", "middle")
        .text("Word")
        .attr("fill", chartText);

    // text label for the y axis
    svgExp.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y",0 - marginSvgExp.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Count")
        .attr("fill", chartText); 
        
    // TITLE text label
    svgExp.append("text")     
        .attr("transform",
            "translate(" + (width/2) + " , -10)")
        .style("text-anchor", "middle")
        .text(chartTitle)
        .attr("class", "chartTitle")
        .attr("fill", chartText);

        
    svgExp.append("g")
        .attr("transform",
            "translate(20 , 20)")
        .attr("class", "top5")
        .append("text")
        .text("Top 5:")
        .attr("class","top5heading")
        .attr("fill", chartText);
        ;
        

    var top5data = expData.slice(0, 5);
    
    for (var i = 0; i < top5data.length; i++) {
        console.log(top5data[i]);
        svgExp.select(".top5")
            .append("text")
            .text(top5data[i].id)
            .attr("dy", (1.2+i*1.2)+"em")
            .attr("fill", chartText);
    }
}