
var sliderSvg = d3.select("svg#slider"),
    margin = {right: 20, left: 20},
    width = +sliderSvg.attr("width") - margin.left - margin.right,
    height = +sliderSvg.attr("height");

var x = d3.scaleLinear()
    .domain([1, 250])
    .range([0, width])
    .clamp(true);

var slider = sliderSvg.append("g")
    .attr("class", "slider")
    .attr("transform", "translate(" + margin.left + "," + height / 2 + ")");

slider.append("line")
    .attr("class", "track")
    .attr("x1", x.range()[0])
    .attr("x2", x.range()[1])
  .select(function() { return this.parentNode.appendChild(this.cloneNode(true)); })
    .attr("class", "track-inset")
  .select(function() { return this.parentNode.appendChild(this.cloneNode(true)); })
    .attr("class", "track-overlay")
    .call(d3.drag()
        .on("start.interrupt", function() { slider.interrupt(); })
        .on("start drag", function() { numCount(x.invert(d3.event.x)); }));

slider.insert("g", ".track-overlay")
    .attr("class", "ticks")
    .attr("transform", "translate(0," + 18 + ")")
  .selectAll("text")
  .data(x.ticks(10))
  .enter().append("text")
    .attr("x", x)
    .attr("fill", chartText)
    .attr("text-anchor", "middle")
    .text(function(d) { return d; });

var handle = slider.insert("circle", ".track-overlay")
    .attr("class", "handle")
    .attr("r", 9);

slider.transition() // Gratuitous intro!
    .duration(750)
    .tween("numCount", function() {
      var i = d3.interpolate(0, initNum);
      return function(t) { numCount(i(t)); };
    });

function numCount(h) {
    initNum = Math.round(h);
    handle.attr("cx", x(h));
    initializeWordCount(initNum);
    initializeWordCountLo(initNum);
    initializeWordCountHi(initNum);
    initializeWordCountExp(initNum);
}

