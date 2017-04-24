! function () {
	var dataTool = {
		version: "1.1.0"
	};
	dataTool.convertDate = function (d) {
		//日期转换
		return d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate() + " " + d.getHours() + ":" + d.getMinutes() + ":" + d.getSeconds();
	}
}();