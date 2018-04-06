
d3.csv("data/pick-a-wine.csv", function(error, myData) {
    if (error) {
        console.log("Error");
    }

    //populate dropdown options with input data
	var dropdownOptions = [];
	myData.forEach(function(d, i){
		if ( dropdownOptions.indexOf(d.designation) == -1) {
			dropdownOptions.push(d.designation);
		}; 
	}); 
	var option = '';
	for (var i=0;i<dropdownOptions.length;i++){
	   option += '<option value="'+ dropdownOptions[i] + '">' + dropdownOptions[i] + '</option>';
	}; 
	$('#pickawine-select option').empty(); //clear old options
	$('#pickawine-select').append(option); //add new options


    //listen to dropdown
	d3.select('#pickawine-select').on("change", function() {

		var dropdown = document.getElementById("pickawine-select");
		var designation_sel = dropdown.options[dropdown.selectedIndex].value;

	    var myArray = [];
	    myData.forEach(function(d, i){
	    	//d.points = +d.points;
	    	//d.price = +d.price;
	        // Add a new array with the values of each:
	        if (d['designation'] == designation_sel) {
	        	myArray.push([d.designation, d.variety, d.winery, d.country, d.description]);
	    	};
	    });
	    //generate table
	    tabulate(myArray, ["designation", "variety", "winery", "country", "description"],'#pickawine-result')

	});


});

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
        .enter()
        .append("td")
        .text(function(d) { return d.value; });
    return table;
};

//http://bl.ocks.org/yan2014/c9dd6919658991d33b87
//http://bl.ocks.org/jhubley/17aa30fd98eb0cc7072f
