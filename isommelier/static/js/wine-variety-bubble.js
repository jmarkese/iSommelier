
var width = 550;
var height = 550;


var svg1 = d3.select("#bubble1")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("font-family", "sans-serif")
    .attr("font-size", "10")
    .attr("text-anchor", "middle")
    .attr("class", "bubble");


// var svg = d3.select("#bubble1 svg"),
//     width = +svg.attr("width"),
//     height = +svg.attr("height");

var format = d3.format(",d");

var color = d3.scaleOrdinal(d3.schemeCategory20c);

var pack1 = d3.pack()
    .size([width, height])
    .padding(1.5); 

d3.csv("../../winereviews/wine_variety_stats/", function(d) {
  d.value = +d.value;
  if (d.value) return d;
}, function(error, classes) {
  if (error) throw error;

  var root = d3.hierarchy({children: classes})
      .sum(function(d) { return d.value; })
      .each(function(d) {
        if (id = d.data.id) {
          var id, i = id.lastIndexOf(".");
          d.id = id;
          // d.package = id.slice(0, i);
          // d.class = id.slice(i + 1);
          d.class = id
        }
      });

  var node = svg1.selectAll(".node")
    .data(pack1(root).leaves())
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

      //newch
  var tooltip = d3.select("body")
      .append("div")
      .style("position", "absolute")
      .style("z-index", "10")
      .style("visibility", "hidden")
      .style("color", "white")
      .style("padding", "8px")
      .style("background-color", "rgba(0, 0, 0, 0.75)")
      .style("border-radius", "6px")
      .style("font", "12px sans-serif")
      .text("tooltip");

  node.append("circle")
      .attr("id", function(d) { return d.id; })
      .attr("r", function(d) { return d.r; })
      // .style("fill", function(d) { return color(d.package); })
      .style("fill", function(d) { return color(d.class); })

      //newch
      .on("mouseover", function(d) {
              tooltip.text(d.class + ": " + format(d.value) + ' reviews'); //not working??
              tooltip.style("visibility", "visible");
      })
      .on("mousemove", function() {
          return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
      })
      .on("mouseout", function(){return tooltip.style("visibility", "hidden");})
      .on("click", function(d){
	    getVarietyReviewData(d.data.varietyId);
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
      .text(function(d) { return d; });

  node.append("title")
      .text(function(d) { return d.id + "\n" + format(d.value); });
});


d3.csv("../../winereviews/variety_options/", function(error, myData) {
    if (error) {
        console.log("Error");
    }

    // populate dropdown options with input data
	var option = '';
	var dropdownOptions = [];
	myData.forEach(function(d, i){
 	   option += '<option value="'+ d.id + '">' + d.name + '</option>';
	});

	$('#pickawine-select option').empty(); //clear old options
	$('#pickawine-select').append(option); //add new options

    //listen to dropdown
	d3.select('#pickawine-select').on("change", function() {

		var dropdown = document.getElementById("pickawine-select");
		var varietyId = dropdown.options[dropdown.selectedIndex].value;
	    getVarietyReviewData(varietyId);

	});

});

function getVarietyReviewData(varietyId) {
    var varietyReviewEndpoint = "../../winereviews/variety_reviews/" + varietyId;
    d3.csv(varietyReviewEndpoint, function(d) {
        return d;
    }, function(data) {

	    var reviewArray = [];
	    data.forEach(function(d, i){
        	reviewArray.push([d.taster, d.points, d.designation, d.variety, d.winery, d.country, d.description, d.id, d.likes, d.flag]);
	    });

	    //generate table
	    tabulate(reviewArray, ["taster", "rating", "designation", "variety", "winery", "country", "description"],'#pickawine-result')
    });
}

function deleteReview(reviewId) {
    console.log(reviewId);
    var reviewDeleteResponse = "../../winereviews/review_delete/" + reviewId;
    d3.request(reviewDeleteResponse)
        .get(function() { console.log("GET"); })
        .response(function(xhr) { console.log(xhr.responseText);
        });
}

function likeReview(reviewId) {
    console.log(reviewId);
    var reviewLikeResponse = "../../winereviews/review_like/" + reviewId;
    d3.request(reviewLikeResponse)
        .get(function() { console.log("GET"); })
        .response(function(xhr) { console.log(xhr.responseText); });
}

function tabulate(data, columns, id) {
    //newch remove existing table
    d3.select(id).select('table').remove();
    var table = d3.select(id).append("table"),
        thead = table.append("thead"),
        tbody = table.append("tbody");

    // append the header row
    thead.append("tr")
        .selectAll("th")
        .data(columns)
        .enter()
        .append("th")
        .text(function(column) { return column; });

    // create a row for each object in the data
    var rows = tbody.selectAll("tr")
        .data(data)
        .enter()
        .append("tr");

    // create a cell in each row for each column
    // At this point, the rows have data associated.
    // So the data function accesses it.
    var cells = rows.selectAll("td")
        .data(function(row) {
            return columns.map(function(d, i) {
                return {value: row[i]};
            });
        })
        // .id(function(row) {
        //     return columns.map(function(d, i) {
        //         return {value: row[i]};
        //     });
        // })
        .enter()
        .append("td")
        .text(function(d) { return d.value; });
    rows.append("td")
            .attr("class", "likebutton")
            .text(function(d){return d[8];});
    rows.append("td")
            .attr("class", "likebutton")
            .append("img")
            .attr("src" ,"../../static/images/like.png")
            .attr("height","30px")
            .on("click", function(d){ likeReview(d[7]); $(this).closest('td').prev().text(++d[8]); });
    rows.append("td")
            .attr("class", "likebutton")
            .text(function(d){return d[9];});
    rows.append("td")
            .attr("class", "likebutton")
            .append("img")
            .attr("src" ,"../../static/images/flag.png")
            .attr("height","30px")
            .on("click", function(d){ deleteReview(d[7]); $(this).closest('td').prev().text(++d[9]);});



    return table;
};

//http://bl.ocks.org/yan2014/c9dd6919658991d33b87
//http://bl.ocks.org/jhubley/17aa30fd98eb0cc7072f
