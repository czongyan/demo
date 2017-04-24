(function () {
	var timeseries = function (spaced, data, firstIndex, secondIndex, enableBrush, enableZoom) {
		var dataSet = new Array();
		data.forEach(function (d) {
			var j = d.index;
			if (j < secondIndex) {
				if (j >= firstIndex) {
					dataSet.push(d);
				}
			}
		});
		render(spaced, dataSet, enableBrush, enableZoom);
	};
	//渲染
	function convertDate(d) {
		return d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate() + " " + d.getHours() + ":" + d.getMinutes() + ":" + d.getSeconds();
	}

	function render(spaced, dataSet, enableBrush, enableZoom) {
		//清空timeMap显示内容；
		var divID = document.getElementById(spaced);
		divID.innerHTML = " ";
		var height = divID.offsetHeight
			, width = divID.offsetWidth
			, margin = {
				top: 20
				, right: 40
				, bottom: 20
				, left: 40
			}
			, timeHeight = height - margin.top - margin.bottom
			, timeWidth = width - margin.left - margin.right;
		var container = d3.select("div#" + spaced).append("svg").attr("width", width).attr("height", height);
		var svg = container.append("g").attr('class', 'content').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
		//定义坐标轴取值范围domain和空间范围range//
		//d3.extent从数组里选出最小值和最大值，d3.max选数组里面最大值
		//横坐标时间
		xExtent = d3.extent(dataSet, function (d, i) {
			return d.date;
		});
		//纵坐标发电功率
		yExtent = [d3.min(dataSet, function (d) {
			return d[selectMap]
		}), d3.max(dataSet, function (d) {
			return d[selectMap];
		})];
		//纵坐标主蒸汽压力
		yMSP = [d3.min(dataSet, function (d) {
			return d.MSP
		}), d3.max(dataSet, function (d) {
			return d.MSP;
		})];
		//纵坐标主蒸汽温度
		yTHRTEMP = [d3.min(dataSet, function (d) {
			return d.THRTEMP
		}), d3.max(dataSet, function (d) {
			return d.THRTEMP;
		})];
		//纵坐标功率负荷
		ySETMW = [d3.min(dataSet, function (d) {
			return d.SETMW
		}), d3.max(dataSet, function (d) {
			return d.SETMW;
		})];
		var x = d3.scaleTime().domain(xExtent).range([0, timeWidth]);
		var y = d3.scaleLinear().domain(yExtent).range([timeHeight, 0]);
		var y1 = d3.scaleLinear().domain(yMSP).range([timeHeight, 0]);
		var y2 = d3.scaleLinear().domain(yTHRTEMP).range([timeHeight, 0]);
		var y3 = d3.scaleLinear().domain(ySETMW).range([timeHeight, 0]);
		//定制x,y轴画布位置
		var xAxis = d3.axisBottom(x).tickFormat(d3.timeFormat("%H:%M"));
		var yAxis = d3.axisLeft(y).ticks(5);
		var yAxis1 = d3.axisRight(y1).ticks(5);
		var yAxis2 = d3.axisRight(y2).ticks(5);
		var yAxis3 = d3.axisLeft(y3).ticks(5);
		//坐标轴加入svg容器
		svg.append("g").attr("class", 'axis axis--x').attr('transform', 'translate(0,' + timeHeight + ')').call(xAxis);
		//增加坐标说明
		//				.append('text').text('时间').attr('transform', 'translate(' + timeWidth + ',0)');
		//左侧纵坐标
		svg.append('g').attr('class', 'axis axis--y').call(yAxis);
		//右侧纵坐标
		svg.append('g').attr('class', 'axis axis--y').call(yAxis1);
		svg.append('g').attr('class', 'axis axis--y').attr('transform', 'translate(' + (timeWidth) + ',0)').call(yAxis2);
		svg.append('g').attr('class', 'axis axis--y').attr('transform', 'translate(' + (timeWidth) + ',0)').call(yAxis3);
		//.append('text').text('发电功率/单位');
		//画线
		//定义线性
		var line = d3.svg.line().x(function (d) {
			return x(d.date);
		}).y(function (d) {
			return y(d.MWValue);
		}).interpolate('monotone');
		var line1 = d3.svg.line().x(function (d) {
			return x(d.date);
		}).y(function (d) {
			return y1(d.MSP);
		}).interpolate('monotone');
		var line2 = d3.svg.line().x(function (d) {
			return x(d.date);
		}).y(function (d) {
			return y2(d.THRTEMP);
		}).interpolate('monotone');
		var line3 = d3.svg.line().x(function (d) {
			return x(d.date);
		}).y(function (d) {
			return y2(d.SETMW);
		}).interpolate('monotone');
		//改变线条相邻两点之间的链接方式以及是否闭合，接受的参数有linear，step-before，step-after，basis，basis-open，basis-closed，bundle，cardinal，cardinal-open，cardinal-closed，monotone
		var path = svg.append('path').datum(dataSet).attr('class', 'line').attr('d', line).on("mouseover", mouseover);
		var path = svg.append('path').datum(dataSet).attr('class', 'line1').attr('d', line1);
		var path = svg.append('path').datum(dataSet).attr('class', 'line2').attr('d', line2);
		var path = svg.append('path').datum(dataSet).attr('class', 'line3').attr('d', line3);

		function mouseover(d) {
			//console.log(d);
			return d.MWValue;
		};
		if (enableBrush) {
			//brush还可以增加brushend的属性，表示brush结束后的动作
			var brush = d3.brushX().extent([[0, 0], [timeWidth, timeHeight]]).on("brush end", brushed);
			//var zoom = d3.zoom().on("zoom", zoomed);
			//定义画布
			var gBrush = svg.append("g").attr("class", "brush").call(brush);
			//			.call(brush.move, x.range());
			var brushEl = '<div class="brush-control"><div class="brush-info"><i class="brush-i">Click and drag on the timeseries to create a brush.</i></div></div>';
			//			<button class="clear-brush">Clear brush</button>
			divID.insertAdjacentHTML('beforeend', brushEl);

			function brushed() {
				if (!d3.event.sourceEvent) return; // Only transition after input.
				if (!d3.event.selection) return;
				//                if (!brush.empty()) {
				//				d3.select('.clear-brush').style("display", "inline-block");
				var s = d3.event.selection || x.range();
				var dm = s.map(x.invert, x);
				$("div.brush-info:first-child i")["0"].innerText = convertDate(dm[0]) + " 至 " + convertDate(dm[1]);
			}
			//			d3.select('.clear-brush').on("click", function (d) {
			//				//console.log(brush.clear());
			//				if (!d3.event.sourceEvent) return; // Only transition after input.
			//				if (!d3.event.selection) return;
			//				d3.selectAll("g.brush").call(brush.clear());
			//				$("div.brush-info:first-child i")["0"].innerText.innerText="";
			//				d3.select('.clear-brush').style("display", "none");
			//			})
			timeseries.getBrushExtent = function () {
				if (brush) return brush.extent();
			}
		};
		if (enableZoom) {
			var zoom = d3.zoom().on("zoom", zoomed);
			svg.append("rect").attr("class", "zoom").attr("width", timeWidth).attr("height", timeHeight).attr("transform", "translate(" + margin.left + "," + margin.top + ")").call(zoom);

			function zoomed() {
				if (d3.event.sourceEvent && d3.event.sourceEvent.type === "brush") return; // ignore zoom-by-brush
				var t = d3.event.transform;
				x1 = t.rescaleX(x);
				focus.select(".line").attr("d", line);
				focus.select(".axis--x").call(xAxis);
				context.select(".brush").call(brush.move, x1.range().map(t.invertX, t));
			}
		}
	}
	if (typeof define === "function" && define.amd) define(timeseries);
	else if (typeof module === "object" && module.exports) module.exports = timeseries;
	this.timeseries = timeseries;
})();