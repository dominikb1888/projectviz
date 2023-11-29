function genHistograms() {
    d3.selectAll(".histogram").each(function(d,i) {
      const grouped = JSON.parse(d3.select(this).attr("data-histogram"));
      var xscale = d3.scaleTime()
          .domain([new Date(2023, 10, 1), new Date(2024, 2, 1)])
          .range([0,120]);
      var yscale = d3.scaleLog([1,10], [1,100]);
      var w = 5
      var h = 10
      var bh = 150
      var bw = 300

      var today = new Date();
      var today_pos = xscale(today) * w
      const svg = d3.select(this)
          .append("svg")
          .attr("viewBox", [0, 0, bw, bh]);

      console.log(grouped)
      svg
        .append("g")
          .attr("fill", "yellowgreen")
        .selectAll("rect")
        .data(grouped)
        .join("rect")
          .attr("x", function (d) { date = new Date(d.date); return xscale(date) * w;})
          .attr("y", (d)  => -(yscale(d.count) - bh))
          .attr("height", (d) => yscale(d.count))
          .attr("width", w + "px")

        svg
          .append('path')
          .attr('d', d3.line()([[today_pos, 0], [today_pos, 300]]))
          .attr('stroke', 'black');

      return this
    });
  }
