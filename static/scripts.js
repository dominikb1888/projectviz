function genHistograms() {
    d3.selectAll(".histogram").each(function(d,i) {
      const grouped = JSON.parse(d3.select(this).attr("data-histogram"));
      var tscale = d3.scaleTime()
          .domain([new Date(2023, 10, 1), new Date(2024, 2, 1)])
          .range([0,120]);

      var w = 5
      var h = 10
      var today = new Date();
      var today_pos = tscale(today) * w

      const svg = d3.select(this)
          .append("svg")
          .attr("viewBox", [0, 0, 300, 150]);

      svg
        .append("g")
          .attr("fill", "yellowgreen")
        .selectAll("rect")
        .data(grouped)
        .join("rect")
          .attr("x", function (d) { date = new Date(d.date); return tscale(date) * w;})
          .attr("y", (d)  => -(d.count * h - 100))
          .attr("height", (d) => d.count * h)
          .attr("width", w + "px")

        svg
          .append('path')
          .attr('d', d3.line()([[today_pos, 0], [today_pos, 300]]))
          .attr('stroke', 'black');

      return this
    });
  }