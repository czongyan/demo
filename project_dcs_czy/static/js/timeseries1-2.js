(function () {
    var version = "1.0.1";
    var timeseries = function (spaced, flag, data, selectDate, typeFlag, enableBrush, enableZoom) {
        var dataSet = new Array();
        //		console.log(data);
        data.forEach(function (d) {
            var j = d.date;
            if (j <= selectDate[1]) {
                if (j >= selectDate[0]) {
                    dataSet.push(d);
                }
            }
        });
        var property_name = d3.keys(data[0]);
        //		console.log(property_name);
        var data_range = new Array(),
            data_domain = new Array();
        for (var i in property_name) {
            if (property_name[i] != "date") {
                data_domain.push(property_name[i]);
                data_range.push(d3.extent(data,  function (d)  { 
                    return  d[property_name[i]]; 
                }));
            }
        };
        csv_range.push([spaced, data_domain, data_range]);
        //			var property_name = d3.keys(dataSet[0]);
        //			data.forEach(function (d) {
        //				for (var j in property_name) {
        //					if (property_name[j] != "date") d[property_name[j]] = parseInt(d[property_name[j]]);
        //				}
        //			});
        var len = dataSet.length;
        var divID = document.getElementById(spaced);
        //		console.log(spaced);
        if (divID.innerHTML != "") divID.innerHTML = "";
        var dateShow = document.createElement('div');
        dateShow.innerHTML = '<div class="time-info" style="height=15px;text-align:center"><i class="time-i">时序图显示时间范围为：' + convertDate(selectDate[0]) + " 至 " + convertDate(selectDate[1]) + '</i></div>';
        //			<button class="clear-brush">Clear brush</button>
        divID.appendChild(dateShow);
        var property_1 = [["发电功率", "MW"]];
        var property_1_0 = [["发电功率", "MW"], ["功率负荷", "MWD2"], ["主蒸汽压力", "MSP"], ["主蒸汽温度", "THRTEMP"]];
        var property_1_1 = [["一次再热汽压", "YRHRPRS"], ["一次再热汽温", "YRHRTEMPT"], ["二次再热汽压", "RRHRPRS"], ["二次再热汽温", "RRHRTEMPT"]];
        var property_1_2 = [["锅炉主控", "BMOUT"]["给水流量", "FWFLOW"], ["给水泵汽机A转速指令", "XYA11"], ["给水泵汽机B转速指令", "XYA21"], ["过热器入口焓值", "A09M210SHH"], ["总煤量", "TOTALCOAL"], ["总风量", "TAF"], ["氧量", "O2"], ["炉膛负压", "SELFP1"], ["排烟温度", "A017P005"]];
        var property_1_3 = [["AB燃烧器摆角1", "HHA11AS001XQ01"], ["AB燃烧器摆角2", "HHA12AS001XQ01"], ["AB燃烧器摆角3", "HHA13AS001XQ01"], ["AB燃烧器摆角4", "HHA14AS001XQ01"], ["CD燃烧器摆角1", "HHA31AS001XQ01"], ["CD燃烧器摆角2", "HHA32AS001XQ01"], ["CD燃烧器摆角3", "HHA33AS001XQ01"], ["CD燃烧器摆角4", "HHA34AS001XQ01"], ["EF燃烧器摆角1", "HHA51AS001XQ01"], ["EF燃烧器摆角2", "HHA52AS001XQ01"], ["EF燃烧器摆角3", "HHA53AS001XQ01"], ["EF燃烧器摆角4", "HHA54AS001XQ01"]];
        var property_1_4 = [["AGP下燃烧器摆角1", "HHA71AS001XQ01"], ["AGP下燃烧器摆角2", "HHA72AS001XQ01"], ["AGP下燃烧器摆角3", "HHA73AS001XQ01"], ["AGP下燃烧器摆角4", "HHA74AS001XQ01"], ["AGP上燃烧器摆角1", "HHA81AS001XQ01"], ["AGP上燃烧器摆角2", "HHA82AS001XQ01"], ["AGP上燃烧器摆角3", "HHA83AS001XQ01"], ["AGP上燃烧器摆角4", "HHA84AS001XQ01"]];
        var property_1_5 = [["一次再热器烟气挡板1", "HNA00AA001AXQ01"], ["一次再热器烟气挡板2", "HNA00AA001BXQ01"], ["二次再热器烟气挡板1", "HNA00AA002AXQ01"], ["二次再热器烟气挡板2", "HNA00AA002BXQ01"]];
        var property_1_6 = [["过热器一级气动减温喷水阀1", "LAE11CG101XQ01"], ["过热器一级气动减温喷水阀2", "LAE12CG101XQ01"], ["过热器一级气动减温喷水阀3", "LAE13CG101XQ01"], ["过热器一级气动减温喷水阀4", "LAE14CG101XQ01"], ["过热器二级气动减温喷水阀1", "LAE21CG101XQ01"], ["过热器二级气动减温喷水阀2", "LAE22CG101XQ01"], ["过热器二级气动减温喷水阀3", "LAE23CG101XQ01"], ["过热器二级气动减温喷水阀4", "LAE24CG101XQ01"]];
        var property_1_7 = [["一次再热器事故喷水气动调节阀A", "LAF01CG101XQ01"], ["一次再热器事故喷水气动调节阀B", "LAF02CG101XQ01"], ["一次再热器微量喷水气动调节阀A", "LAF11CG101XQ01"], ["一次再热器微量喷水气动调节阀B", "LAF12CG101XQ01"], ["一次再热器事故喷水气动调节阀C", "LAF13CG101XQ01"], ["一次再热器事故喷水气动调节阀D", "LAF14CG101XQ01"], ["二次再热器事故喷水气动调节阀A", "LAF21CG101XQ01"], ["二次再热器事故喷水气动调节阀B", "LAF22CG101XQ01"], ["二次再热器微量喷水气动调节阀A", "LAF31CG101XQ01"], ["二次再热器微量喷水气动调节阀B", "LAF32CG101XQ01"], ["二次再热器事故喷水气动调节阀C", "LAF33CG101XQ01"], ["二次再热器事故喷水气动调节阀D", "LAF34CG101XQ01"]];
        var property_data = new Array(),
            property_show = new Array();
        switch (typeFlag) {
            case 0:
                if (flag == 1) {
                    for (var i in property_1_0) {
                        property_show.push(property_1_0[i][0]);
                        property_data.push(property_1_0[i][1]);
                    }
                    render(divID, spaced, dataSet, property_show, property_data, enableBrush, enableZoom);
                    divID.style.cssText += "border-right:2px solid #ccc";
                    //				render(divID, spaced, dataSet, enableBrush, enableZoom);
                } else
                if (flag == 2) {
                    for (var i in property_1_1) {
                        property_show.push(property_1_1[i][0]);
                        property_data.push(property_1_1[i][1]);
                    }
                    render(divID, spaced, dataSet, property_show, property_data, enableBrush, enableZoom);
                }
                break;
            case 1:
                brush_obj.push(renderPramater(spaced, dataSet, enableBrush, enableZoom));
                break;
        }
    }; //渲染
    function convertDate(d) {
        return d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate() + " " + d.getHours() + ":" + d.getMinutes() + ":" + d.getSeconds();
    }

    function convertDoubleToInt(d) {
        return parseInt(+d);
    }

    function render(divID, spaced, dataSet, property_show, property_data, enableBrush, enableZoom) {
        //清空timeMap显示内容；
        var height = divID.offsetHeight,
            width = divID.offsetWidth,
            margin = {
                top: 20,
                right: 40,
                bottom: 20,
                left: 40
            },
            timeHeight = height - margin.top - margin.bottom,
            timeWidth = width - margin.left - margin.right;
        var extents = [0, 0],
            gBrush;
        var line_color = d3.scale.category10();
        var line_div = parseInt(spaced.split('_')[2]) - 1;
        var container = d3.select("div#" + spaced).append("svg").attr("class", "line_svg").attr("width", width).attr("height", height);
        var svg = container.append("g").attr('class', 'line_g').attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
        //定义坐标轴取值范围domain和空间范围range//
        //d3.extent从数组里选出最小值和最大值，d3.max选数组里面最大值
        //横坐标时间
        xExtent = d3.extent(dataSet, function (d, i) {
            return d.date;
        });
        //纵坐标发电功率
        yExtent1 = [d3.min(dataSet, function (d) {
            return d[property_data[0]];
        }), d3.max(dataSet, function (d) {
            return d[property_data[0]];
        })];
        //纵坐标主蒸汽压力
        yExtent2 = [d3.min(dataSet, function (d) {
            return d[property_data[1]];
        }), d3.max(dataSet, function (d) {
            return d[property_data[1]];
        })];
        //纵坐标主蒸汽温度
        yExtent3 = [d3.min(dataSet, function (d) {
            return d[property_data[2]];
        }), d3.max(dataSet, function (d) {
            return d[property_data[2]];
        })];
        //纵坐标功率负荷
        yExtent4 = [d3.min(dataSet, function (d) {
            return d[property_data[3]];
        }), d3.max(dataSet, function (d) {
            return d[property_data[3]];
        })];
        var x = d3.time.scale().domain(xExtent).range([0, timeWidth]);
        var y = d3.scale.linear().domain(yExtent1).range([timeHeight, 0]);
        var y1 = d3.scale.linear().domain(yExtent2).range([timeHeight, 0]);
        var y2 = d3.scale.linear().domain(yExtent3).range([timeHeight, 0]);
        var y3 = d3.scale.linear().domain(yExtent4).range([timeHeight, 0]);
        //定制x,y轴画布位置
        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom").tickFormat(d3.time.format("%H:%M"));
        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left").ticks(5);
        var yAxis1 = d3.svg.axis()
            .scale(y1)
            .orient("right").ticks(5);
        var yAxis2 = d3.svg.axis()
            .scale(y2)
            .orient("left").ticks(5);
        var yAxis3 = d3.svg.axis()
            .scale(y3)
            .orient("right").ticks(5);
        //初始化不同属性分别对应的颜色
        line_color.domain = (d3.keys(dataSet[0]).filter(function (key) {
            return key != "date";
        }));
        //坐标轴加入svg容器
        svg.append("g").attr("class", 'axis axis--x').attr('transform', 'translate(0,' + timeHeight + ')').call(xAxis);
        //增加坐标说明
        //				.append('text').text('时间').attr('transform', 'translate(' + timeWidth + ',0)');
        //一轴左侧纵坐标
        svg.append('g').attr('class', 'axis axis--y').call(yAxis).append("text").attr("text-anchor",  "start").attr("x", -(margin.left)).attr("y",  -6).text(property_data[0]).style("fill", "black");
        //一轴右侧纵坐标
        svg.append('g').attr('class', 'axis axis--y').call(yAxis1).append("text").attr("text-anchor", "middle").attr("x", (margin.left - 10)).attr("y", -9).text(property_data[1]).style("fill", "black");
        //二轴左侧纵坐标		
        svg.append('g').attr('class', 'axis axis--y').attr('transform', 'translate(' + (timeWidth) + ',0)').call(yAxis2).append("text").attr("text-anchor", "middle").attr("x", -(margin.left)).attr("y", -9).text(property_data[2]).style("fill", "black");
        //二轴右侧纵坐标	
        svg.append('g').attr('class', 'axis axis--y').attr('transform', 'translate(' + (timeWidth) + ',0)').call(yAxis3).append("text").attr("text-anchor", "middle").attr("x", (margin.left - 10)).attr("y", -9).text(property_data[3]).style("fill", "black");
        //画线
        //定义线性
        var line = d3.svg.line().x(function (d) {
            return x(d.date);
        }).y(function (d) {
            return y(d[property_data[0]]);
        });
        var line1 = d3.svg.line().x(function (d) {
            return x(d.date);
        }).y(function (d) {
            return y1(d[property_data[1]]);
        });
        var line2 = d3.svg.line().x(function (d) {
            return x(d.date);
        }).y(function (d) {
            return y2(d[property_data[2]]);
        });
        var line3 = d3.svg.line().x(function (d) {
            return x(d.date);
        }).y(function (d) {
            return y3(d[property_data[3]]);
        });
        //改变线条相邻两点之间的链接方式以及是否闭合，接受的参数有linear，step-before，step-after，basis，basis-open，basis-closed，bundle，cardinal，cardinal-open，cardinal-closed，monotone
        var path = svg.append('path').datum(dataSet).attr('class', 'line').attr('d', line).style("stroke", function (d) {
            return line_color(property_data[0])
        });
        var path = svg.append('path').datum(dataSet).attr('class', 'line1').attr('d', line1).style("stroke", function (d) {
            return line_color(property_data[1])
        });
        var path = svg.append('path').datum(dataSet).attr('class', 'line2').attr('d', line2).style("stroke", function (d) {
            return line_color(property_data[2])
        });
        var path = svg.append('path').datum(dataSet).attr('class', 'line3').attr('d', line3).style("stroke", function (d) {
            return line_color(property_data[3])
        });

        function mouseover(d) {
            //console.log(d);
            return d.MW;
        };
        var tipsEl = '<div class="line-tip" style="height:35px;"><label class="line1-tip" style="float:left;width:150px;text-align:right">' + property_show[0] + '</label> <HR style="background-color:' + line_color(property_data[0]) + ';float:left;margin-left:5px;border:0" width="60px" SIZE=3> <label class="line1-tip" style="float:left;width:150px;text-align:right">' + property_show[1] + '</label><hr style="background-color:' + line_color(property_data[1]) + ';float:left;margin-left:5px;border:0" width="60px;margin-left:10px" SIZE=3></hr><br/>		<label class="line1-tip" style="float:left;width:150px;text-align:right">' + property_show[2] + '</label><hr style="background-color:' + line_color(property_data[2]) + ';float:left;margin-left:5px;border:0" width="60px" SIZE=3></hr><label class="line1-tip" style="float:left;width:150px;text-align:right">' + property_show[3] + '</label><hr style="background-color:' + line_color(property_data[3]) + ';float:left;margin-left:5px;border:0" width="60px" SIZE=3></hr></div>';
        divID.insertAdjacentHTML('beforeend', tipsEl);
        $(".line-tip").width = timeHeight;
        var move_extents = [0, 0];
        if (enableBrush) {
            //brush还可以增加brushend的属性，表示brush结束后的动作
            var brush = d3.svg.brush().x(x).on("brush", brushed).on("brushend", brushend);
            //var zoom = d3.zoom().on("zoom", zoomed);
            //定义画布
            gBrush = svg.append("g").attr("class", "brush").call(brush).selectAll("rect").attr("y",  -6).attr("height",  timeHeight + 7); 
            //			.call(brush.move, x.range());
            var brushEl = '<div class="brush-control"><div class="brush-info-' + line_div + '"><i class="brush-i">Click and drag on the timeseries to create a brush.</i></div></div>';
            divID.insertAdjacentHTML('beforeend', brushEl);

            function brushed() {
                //for()
                line_brush_selection[line_div][1] = true;
                if (!d3.event.sourceEvent) return; // Only transition after input.
                if (!d3.event.selection) return;
                var s = d3.event.selection || x.range();
                var dm = s.map(x.invert, x);
                console.log("开始")
                line_obj[line_div] = dm;
                for (var i in line_brush_selection) {
                    if (line_obj[i][0] == 0 && line_obj[i][1] == 0) {
                        if (line_brush_selection[i][0] != spaced && line_brush_selection[i][1] == false) {
                            d3.select("div#" + line_brush_selection[i][0] + " .brush").call(brush.move, [s[0], s[1]]);
                            line_brush_selection[i][1] = true;
                        }
                    }
                }
                //				brush_line_move(spaced, d3.event.selection);
            }

            function brushend() {
                var s = d3.event.selection || x.range();
                var t = d3.event.transform;
        //				x1 = t.rescaleX(x);
                var dm = s.map(x.invert, x);
                line_obj[line_div] = dm;
                for (var i in line_brush_selection) {
                    if (line_obj[i][0] == 0 && line_obj[i][1] == 0) {
                        if (line_brush_selection[i][0] != spaced && line_brush_selection[i][1] == false) {
//                            d3.select("div#" + line_brush_selection[i][0] + " .brush").call(brush.move,x.range().map(dm[1], t));
                            line_brush_selection[i][1] = true;
                        }
                    }
                }
                if (line_obj[line_div][0] != 0 && line_obj[line_div][1] != 0 && line_brush_selection[line_div][1] == true) {
                    $("div.brush-info-" + line_div + ":first-child i")["0"].innerText = convertDate(dm[0]) + " 至 " + convertDate(dm[1]);
                    brush_all(line_div, 1);
                    brush_display();
                }
            }
        };
        //		if (enableZoom) {
        //			var zoom = d3.zoom().on("zoom", zoomed);
        //			svg.append("rect").attr("class", "zoom").attr("width", timeWidth).attr("height", timeHeight).attr("transform", "translate(" + margin.left + "," + margin.top + ")").call(zoom);
        //
        //			function zoomed() {
        //				if (d3.event.sourceEvent && d3.event.sourceEvent.type === "brush") return; // ignore zoom-by-brush
        //				var t = d3.event.transform;
        //				x1 = t.rescaleX(x);
        //				focus.select(".line").attr("d", line);
        //				focus.select(".axis--x").call(xAxis);
        //				context.select(".brush").call(brush.move, x1.range().map(t.invertX, t));
        //			}
        //		}
        line_brush_selection.push([spaced, false]);
        line_obj.push(extents);
    }

    function brush_line_move(d, m) {
        var brush = d3.brushX().extent([[0, 0], [0, 0]]).on("brush end", brushed);
        for (var i in line_brush_selection) {
            if (line_brush_selection[i][0] != d && line_brush_selection[i][1] == false) {
                d3.select("div#" + d + " .brush").call(brush.clamp([m[0], m[1]]));
            }
        }
    }

    function renderPramater(spaced, dataSet, enableBrush, enableZoom) {
        var divID = document.getElementById(spaced);
        var margin = {
                top: 20,
                right: 10,
                bottom: 10,
                left: 40
            },
            width = divID.offsetWidth - margin.left - margin.right,
            height = divID.offsetHeight - margin.top - margin.bottom;
        //var x = d3.scalePoint().range([0, width])
        var x = d3.scaleBand().rangeRound([0, width]).padding(1),
            y = {},
            dragging = {};
        var line = d3.line(),
            axis = d3.axisLeft(),
            background, foreground, extents;
        var coordinate_div = parseInt(spaced.split('_')[1]) - 1;
        var svg = d3.select("div#" + spaced).append("svg").attr("class", "coordinate_svg").attr("width", width + margin.left + margin.right).attr("height", height + margin.top + margin.bottom).append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        x.domain(dimensions = d3.keys(dataSet[0]).filter(function (d) {
            if (d == "num") return false;
            else if (d == "date") return (y[d] = d3.scaleTime().domain(d3.extent(dataSet, function (p) {
                return +p[d];
            })).range([height, 0]));
            else return (y[d] = d3.scaleLinear().domain(d3.extent(dataSet, function (p) {
                return +p[d];
            })).range([height, 0]));
        }));
        extents = dimensions.map(function (p) {
            return [0, 0];
        });
        // Add grey background lines for context.
        background = svg.append("g").attr("class", "background").selectAll("path").data(dataSet).enter().append("path").attr("d", path);
        // Add blue foreground lines for focus.
        foreground = svg.append("g").attr("class", "foreground").selectAll("path").data(dataSet).enter().append("path").attr("d", path);
        // Add a group element for each dimension.
        var g = svg.selectAll(".dimension").data(dimensions).enter().append("g").attr("class", "dimension").attr("transform", function (d) {
            return "translate(" + x(d) + ")";
        }).call(d3.drag().on("start", function (d) {
            dragging[d] = this.__origin__ = x(d);
            background.attr("visibility", "hidden");
        }).on("drag", function (d) {
            dragging[d] = Math.min(w, Math.max(0, this.__origin__ += d3.event.dx));
            foreground.attr("d", path);
            dimensions.sort(function (a, b) {
                return position(a) - position(b);
            });
            x.domain(dimensions);
            g.attr("transform", function (d) {
                return "translate(" + position(d) + ")";
            })
        }).on("end", function (d) {
            delete this.__origin__;
            delete dragging[d];
            transition(d3.select(this)).attr("transform", "translate(" + x(d) + ")");
            transition(foreground).attr("d", path);
            background.attr("d", path).transition().delay(500).duration(0).attr("visibility", null);
        }));
        // Add an axis and title.
        g.append("g").attr("class", "coordinate_axis").each(function (d) {
            d3.select(this).call(axis.scale(y[d]));
        }).append("text").attr("text-anchor", "middle").attr("y", -9).text(String);
        if (enableBrush) {
            // Add and store a brush for each axis.
            g.append("g").attr("class", "coordinate_brush").each(function (d) {
                d3.select(this).call(y[d].brush = d3.brushY().extent([[-8, 0], [8, height]]).on("start", brushstart).on("brush end", brush));
            }).selectAll("rect").attr("x", -8).attr("width", 16);
        }

        function position(d) {
            var v = dragging[d];
            return v == null ? x(d) : v;
        }

        function transition(g) {
            return g.transition().duration(500);
        }
        // Returns the path for a given data point.
        function path(d) {
            return line(dimensions.map(function (p) {
                return [position(p), y[p](d[p])];
            }));
        }
        // When brushing, don’t trigger axis dragging.
        function brushstart() {
            d3.event.sourceEvent.stopPropagation();
        }
        // Handles a brush event, toggling the display of foreground lines.
        function brush() {
            for (var i in brush_obj[coordinate_div][0]) {
                if (d3.event.target == brush_obj[coordinate_div][1][brush_obj[coordinate_div][0][i]].brush) {
                    if (d3.event.selection == null) brush_obj[coordinate_div][2][i] = [0, 0];
                    else {
                        brush_obj[coordinate_div][2][i] = d3.event.selection.map(brush_obj[coordinate_div][1][brush_obj[coordinate_div][0][i]].invert, brush_obj[coordinate_div][1][brush_obj[coordinate_div][0][i]]);
                    }
                }
            }
            brush_all(coordinate_div, 2);
            brush_display();
        }
        brush_foreground.push(foreground);
        return ([dimensions, y, extents]);
    }

    function brush_display() {
        for (var t in brush_foreground) {
            brush_foreground[t].style("display", function (d) {
                //none为不显示
                return brush_obj[t][0].every(function (p, i) {
                    if (brush_obj[t][2][i][0] == 0 && brush_obj[t][2][i][1] == 0) return true;
                    else {
                        return brush_obj[t][2][i][1] <= d[p] && d[p] <= brush_obj[t][2][i][0]
                    };
                }) ? null : "none";
            });
        }
    }

    function brush_all(d, k) {
        var index = 0;
        switch (k) {
            case 1:
                for (var i in brush_obj[0][0]) {
                    if (brush_obj[0][0][i] == "date") index = i;
                }
                //			for (var i in line_obj) {
                //				if (i != d) line_obj[i] = line_obj[d];
                //			}
                for (var i in brush_obj) {
                    brush_obj[i][2][index][0] = line_obj[d][1];
                    brush_obj[i][2][index][1] = line_obj[d][0];
                }
                break;
            case 2:
                for (var i in brush_obj[d][0]) {
                    if (brush_obj[d][0][i] == "date") index = i;
                }
                for (var i in brush_obj) {
                    if (i != d) {
                        brush_obj[i][2][index] = brush_obj[d][2][index];
                    }
                }
                //			for (var i in line_obj) {
                //				line_obj[i][0] = brush_obj[d][2][index][1];
                //				line_obj[i][1] = brush_obj[d][2][index][0];
                //			}
                break;
        }
    }

    function typeEF(d, i) {
        d.date = parseDate(d.date);
        d.num = ++i;
        return d;
    }
    if (typeof define === "function" && define.amd) define(timeseries);
    else if (typeof module === "object" && module.exports) module.exports = timeseries;
    this.timeseries = timeseries;
})();