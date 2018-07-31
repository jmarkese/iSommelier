var wordData = {};

d3.queue()
    .defer(d3.csv, "../../winereviews/word_count_stats/500")
    .await(analyze);

function analyze(error, words) {
    if(error) { console.log(error); }
    wordData = words;
    initializeWordCount(initNum);
}

function initializeWordCount (number) {

    var marginBubble = {top: 30, right: null, bottom: null, left: null};


    dataSlice = wordData.slice(0, number);
    
    d3.selectAll("#bubble1 > *").remove();
    
    var width = 400;
    var height = 400;
    var chartTitle = "Top "+number+" Words Used Overall";

    var svg1 = d3.select("#bubble1")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("fill", chartText)
        .attr("text-anchor", "middle")
        .attr("class", "")
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0 400 450")
    ;
    
    // var format = d3.format(",d");
    
    var color = d3.scaleOrdinal(d3.schemeCategory20b);
    
    var pack1 = d3.pack()
        .size([width, height])
        // .padding(1.5)
    ;

    var root = d3.hierarchy({children: dataSlice})
        .sum(function(d) { return d.value; })
        .each(function(d) {
            if (id = d.data.id) {
                var id, i = id.lastIndexOf(".");
                d.id = id;
                d.class = id
            }
        });

    var node = svg1.selectAll(".node")
        .data(pack1(root).leaves())
        .enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "translate(" + d.x + "," + (d.y + marginBubble.top) + ")"; });

    node.append("circle")
        .attr("id", function(d) { return d.id; })
        .attr("class", function(d) { return d.id + " searchFunction"; })
        .attr("r", function(d) { return d.r; })
        .attr("opacity", opacityStart)
        .style("fill", function(d) { return color(d.class); })
        .on("mouseover", function(d) {

            d3.selectAll("."+d.id)
                .attr("opacity", opacityRollover);

            tooltip.text(d.class + " : " + format(d.value)); 
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


    node.append("clipPath")
        .attr("id", function(d) { return "clip-" + d.id; })
        .append("use")
        .attr("xlink:href", function(d) { return "#" + d.id; });

    node.append("text")
        .attr("clip-path", function(d) { return "url(#clip-" + d.id + ")"; })
        .selectAll("tspan")
        .data(function(d) { return d.class.split(/(?=[A-Z][^A-Z])/g); })
        .enter().append("tspan")
        .attr("x", 0)
        .attr("y", function(d, i, nodes) { return 13 + (i - nodes.length / 2 - 0.5) * 10; })
        .attr("font-size", "12")
        .attr("fill", "#333")
        .text(function(d) { return d; });

    node.append("title")
        .text(function(d) { return d.id + "\n" + format(d.value); });
        
        
    // TITLE text label
    svg1.append("text")   
        .attr("transform",
            "translate(" + (width/2) + " , 20)")
        .style("text-anchor", "middle")
        .text(chartTitle)
        .attr("class","chartTitle")
        .attr("fill", chartText);



    
}

