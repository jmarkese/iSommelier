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
        	reviewArray.push([d.taster, d.points, d.designation, d.variety, d.winery, d.country, d.description, d.id, d.likes]);
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
        .response(function(xhr) { console.log(xhr.responseText); });
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
            .append("img")
            .attr("src" ,"../../static/images/like.png")
            .attr("height","30px")
            .on("click", function(d){ alert("Thanks for liking. This review now has " + ++d[8] + "!"); likeReview(d[7]); });

    rows.append("td")
            .attr("class", "button")
            .append("button")
            .text(function(d){return "Delete"})
            .on("click", function(d){ $(this).closest('tr').remove(); deleteReview(d[7]); });
            
    return table;
};

//http://bl.ocks.org/yan2014/c9dd6919658991d33b87
//http://bl.ocks.org/jhubley/17aa30fd98eb0cc7072f
