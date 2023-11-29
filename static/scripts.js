function genHistograms() {
    d3.selectAll(".histogram").each(function(d,i) {
      const grouped = JSON.parse(d3.select(this).attr("data-histogram"));
      var xscale = d3.scaleTime()
          .domain([new Date(2023, 10, 1), new Date(2024, 2, 1)])
          .range([0,120]);
      var yscale = d3.scaleLog([1,10], [1,30]);
      var w = 10
      var h = 10
      var bh = 70
      var bw = 300

      var today = new Date();
      var today_pos = xscale(today) * w
    
      var tooltip = d3.select('.tooltip-area')
        .style('opacity', 0)
        .style('display', 'block')
        .style('position', 'absolute')
        .style('z-index', 100);

      const mouseover = (event, d) => {
        tooltip.style("opacity", 1);
      };

      const mouseleave = (event, d) => {
        tooltip.style('opacity', 0);
      }

      const mousemove = (event, d) => {
        const text = d3.select('.tooltip-area__text');
        text.text(d.count);
        const [x, y] = d3.pointer(event,"body");
   
        tooltip
          .style('left', x+5 + "px")
          .style('top', y-33 + "px");
      };


      const svg = d3.select(this)
          .append("svg")
          .attr("viewBox", [0, 0, bw, bh]);

      svg
        .append("g")
          .attr("fill", "rgb(13, 110, 253)")
        .selectAll("rect")
        .data(grouped)
        .join("rect")
          .attr("x", function (d) { date = new Date(d.date); return xscale(date) * w;})
          .attr("y", (d)  => -(yscale(d.count) - bh + 5))
          .attr("height", (d) => yscale(d.count) + 5)
          .attr("width", w + "px")
          .attr("class", "text-bg-success p-3")
          .text(d => d.count)
          .on("mousemove", mousemove)
          .on("mouseleave", mouseleave)
          .on("mouseover", mouseover);

        svg
          .append('path')
          .attr('d', d3.line()([[today_pos, 0], [today_pos, bh]]))
          .attr('stroke', "rgb(13, 110, 253)");

      return this
    });
  }
