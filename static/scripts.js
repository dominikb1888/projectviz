function genHistograms() {
    d3.selectAll(".histogram").each(function(d,i) {
      const grouped = JSON.parse(d3.select(this).attr("data-histogram"));
      const vals = Array.from(Object.values(grouped))
      console.log(grouped)
      const svg = d3.select(this).append("svg")
        .attr("viewBox", [0, 0, 300, 150]);
      const today = new Date().toJSON().slice(0, 10);
      const keys = Object.keys(grouped)
      const today_index = keys.indexOf(today) + 1
      const today_x = (today_index) * 5 - 200

      svg
        .append("g")
          .attr("fill", "yellowgreen")
        .selectAll("rect")
        .data(vals)
        .join("rect")
          .attr("x", (d, i) => i*5 - 200)
          .attr("y", (d, i)  => -(d*10 - 100))
          .attr("height", (d, i)  => d * 10)
          .attr("width", "5px");
      svg
        .append('path')
          .attr('d', d3.line()([[today_x, 0], [today_x, 300]]))
          .attr('stroke', 'black')
          .attr("width", "5px");

      return this
    });
  }