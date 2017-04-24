function draw() {
	//加载像素热力图
	document.getElementById("calendar").innerHTML = "";
	cellSize = document.getElementById("pixleSize").value; // cell size
	cellheight = $("#pixleHeight").val();
	strokeSize = $("#strokeSize").val();
	var obj = document.getElementById("selectMap");
	selectMap  =  obj.options[obj.options.selectedIndex].value;  //这是取值 
	var width = 299 * cellSize
		, height = 600;
	var svg = d3.select("div#calendar");
	var layer = 1;
	for (var j in csv_nest) {
		layer++;
	}
	//			var rectSVG = svg.append("svg").attr("width", width).attr("height", layer * cellheight).attr("class", "MW");
	var rectSVG = svg.append("svg").attr("width", width).attr("class", "MW");
	var rectG = rectSVG.append('g').attr('class', 'rect -g').attr("transform", "translate(5,0)");
	//			console.log("***");
	for (var j in csv_nest) {
		drawRect(csv_nest[j].values, j, rectG);
	}
	//console.log(num);
	var aN = new Array();
	for (var i in num) {
		aN.push(num[i][selectMap])
	}
	return "平均值：" + d3.mean(aN).toFixed(2) + "  最大值：" + d3.max(aN) + "  最小值：" + d3.min(aN);
}
//确定像素块Y坐标位置
function getY(d) {
	return d * cellheight;
}
//获取所属组的时间点y-m-s
function readDate(d) {
	return d.keyDate;
}
//绘制小方块像素点
function drawRect(data, c, rectG) {
	var flag = false;
	for (var i in data) {
		if (data[i].date >= selectS && data[i].date <= selectE) {
			num.push(data[i]);
			flag = true;
		}
	}
	color.domain(d3.extent(num, function (d) {
		return d[selectMap];
	}));
	if (flag) {
		var ty = cellSize - 2;
		var rect = rectG.append('g').selectAll(".minute").data(num).enter().append("rect").attr('id', function (d) {
				//					console.log(d[selectMap]);
				return 'rect-' + d.index
			}).attr("class", "minute").attr("width", cellSize).attr("height", cellheight).attr("x", function (d) {
				return (d.date.getHours() * 12 + d.date.getMinutes() / 5) * cellSize;
			}).attr("y", getY(c)).style("fill", function (d) {
				return compute(color(d[selectMap]));
			}).style("stroke-width", strokeSize)
			//.on("mouseover",mouseover)
			.on("mousedown", mouseDown);
		rect.append("title").text(function (d) {
			return d.keyDate + " " + d.date.getHours() + ":" + d.date.getMinutes() + "  发电功率为:" + d[selectMap];
		});
	}
}

function mouseDown(d) {
	if (drawflag == 0) {
		firstIndex = d.index;
		a[0] = d.date;
	}
	drawflag++;
	if (drawflag == 2) {
		d3.selectAll('rect').style("opacity", 0.5);
		if (d.index <= firstIndex) {
			alert("选取时间点小于前一个,请重新选择");
			drawflag = 1;
		}
		else {
			secondIndex = d.index;
			//选中的rect改变透明度
			var rect = d3.selectAll(rect);
			for (var i = firstIndex; i <= secondIndex; i++) {
				$("#rect-" + i).css("opacity", 1.0);
				//$("#rect-" + i).css("stroke",'blue');
				//console.log(rect[i].id);
			}
			a[1] = d.date;
			var j = d.index;
			//					drawTime(csv_data);
			timeseries('timeseries', csv_data, firstIndex, secondIndex, true);
			drawflag = 0;
		}
	}
}