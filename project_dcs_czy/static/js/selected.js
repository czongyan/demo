(function () {
	selectTool_init = function (t, y, m, d) {
		//年
		//    var year=new Date().getFullYear();    
		//    for(var i=year;i>=1990;i--){
		//        y.options[year+1-i]=new Option(i,i);    //第一个参数是option的文本值，第二个参数是option的value值
		//    }
		//月
		var select_1_file = [["mpt20160301", "发电功率等"], ["", "再热气温气压"], ["", "锅炉主控各参数"], ["angleABCDEF_march_1min", "AB-CD-EF燃烧器摆角1"], ["AGP_march_1min", "AGP上、下燃烧器摆角1234"], ["smoke_march_1min", "一、二次再热器烟气挡板12"], ["water_march_1min", "过热器一、二级气动减温喷水阀1234"]];
		//	var select_1_file = ["mpt201603", "ADBurner201603", "AGP201603", "EFBurner201603", "FAccident201603", "FGDampe201603", "SAccident201603", "superHeat201603"];
		var select_5_file = [["mpt20160305", "发电功率等"]];
//		var select1_len = y.options.length;
		var select_file = function () {
				m.innerHTML = "";
				m.options[0] = new Option("请选择文件", "");
				var flag = y.options[y.options.selectedIndex].value
				switch (flag) {
				case "1":
					var p = 0
						, q = 1;
					for (var j in select_1_file) {
						m.options[q++] = new Option(select_1_file[p][1], p + "," + select_1_file[p][0]);
						p++;
					}
					break;
				case "5":
					var p = 0
						, q = 1;
					for (var j in select_5_file) {
						m.options[q++] = new Option(select_5_file[p][1], p + "," + select_5_file[p][0]);
						p++;
					}
					break;
				}
			}
			//属性数据集
		var property_1_0 = [["发电功率", "MWValue"], ["负荷指令", "SETMW"], ["主蒸汽压力", "MSP"], ["主蒸汽压力设定值", "MSPS"], ["主蒸汽温度", "THRTEMP"]];
		var property_1_3 = [["AB燃烧器摆角1", "HHA11"], ["AB燃烧器摆角2", "HHA12"], ["AB燃烧器摆角3", "HHA13"], ["AB燃烧器摆角4", "HHA14"], ["CD燃烧器摆角1", "HHA31"], ["CD燃烧器摆角2", "HHA32"], ["CD燃烧器摆角3", "HHA33"], ["CD燃烧器摆角4", "HHA34"], ["EF燃烧器摆角1", "HHA51"], ["EF燃烧器摆角2", "HHA52"], ["EF燃烧器摆角3", "HHA53"], ["EF燃烧器摆角4", "HHA54"]];
		var property_1_4 = [["AGP下燃烧器摆角1", "HHA71"], ["AGP下燃烧器摆角2", "HHA72"], ["AGP下燃烧器摆角3", "HHA73"], ["AGP下燃烧器摆角4", "HHA74"], ["AGP上燃烧器摆角1", "HHA81"], ["AGP上燃烧器摆角2", "HHA82"], ["AGP上燃烧器摆角3", "HHA83"], ["AGP上燃烧器摆角4", "HHA84"]];
		var property_1_5 = [["一次再热器烟气挡板1", "HNA00AA001AXQ01"], ["一次再热器烟气挡板2", "HNA00AA001BXQ01"], ["二次再热器烟气挡板1", "HNA00AA002AXQ01"], ["二次再热器烟气挡板2", "HNA00AA002BXQ01"]];
		var property_1_6 = [["过热器一级气动减温喷水阀1", "LAE11"], ["过热器一级气动减温喷水阀2", "LAE12"], ["过热器一级气动减温喷水阀3", "LAE13"], ["过热器一级气动减温喷水阀4", "LAE14"], ["过热器二级气动减温喷水阀1", "LAE21"], ["过热器二级气动减温喷水阀2", "LAE22"], ["过热器二级气动减温喷水阀3", "LAE23"], ["过热器二级气动减温喷水阀4", "LAE24"]];
		var property_1_7 = [["一次再热器事故喷水气动调节阀A", "LAF01"], ["一次再热器事故喷水气动调节阀B", "LAF02"], ["一次再热器微量喷水气动调节阀A", "LAF11"], ["一次再热器微量喷水气动调节阀B", "LAF12"], ["一次再热器事故喷水气动调节阀C", "LAF13"], ["一次再热器事故喷水气动调节阀D", "LAF14"], ["二次再热器事故喷水气动调节阀A", "LAF21"], ["二次再热器事故喷水气动调节阀B", "LAF22"], ["二次再热器微量喷水气动调节阀A", "LAF31"], ["二次再热器微量喷水气动调节阀B", "LAF32"], ["二次再热器事故喷水气动调节阀C", "LAF33"], ["二次再热器事故喷水气动调节阀D", "LAF34"]];
		//属性
		var select_property_1 = function () {
			d.innerHTML = ""; //初始化
			d.style.display = "block";
			d.options[0] = new Option("请选择显示属性", "");
			var y_value = y.value
				, m_value = m.value;
			if (y_value == "" || m_value == "") {
				return;
			}
			else {
				var str = m_value.split(",");
				var flag = str[0]
					, fileName = str[1];
				switch (y_value) {
				case "1":
					switch (flag) {
					case "0":
						var p = 0
							, q = 1;
						for (var j in property_1_0) {
							d.options[q++] = new Option(property_1_0[p][0], property_1_0[p][1]);
							p++;
						}
						break;
					case "1":
						var p = 0
							, q = 1;
						for (var j in property_1_1) {
							d.options[q++] = new Option(property_1_1[p][0], property_1_1[p][1]);
							p++;
						}
						break;
					case "2":
						var p = 0
							, q = 1;
						for (var j in property_1_2) {
							d.options[q++] = new Option(property_2_0[p][0], property_2_0[p][1]);
							p++;
						}
						break;
					case "3":
						var p = 0
							, q = 1;
						for (var j in property_1_3) {
							d.options[q++] = new Option(property_1_3[p][0], property_1_3[p][1]);
							p++;
						}
						break;
					case "4":
						var p = 0
							, q = 1;
						for (var j in property_1_4) {
							d.options[q++] = new Option(property_1_4[p][0], property_1_4[p][1]);
							p++;
						}
						break;
					case "5":
						var p = 0
							, q = 1;
						for (var j in property_1_5) {
							d.options[q++] = new Option(property_1_5[p][0], property_1_5[p][1]);
							p++;
						}
						break;
					case "6":
						var p = 0
							, q = 1;
						for (var j in property_1_6) {
							d.options[q++] = new Option(property_1_6[p][0], property_1_6[p][1]);
							p++;
						}
						break;
					case "7":
						var p = 0
							, q = 1;
						for (var j in property_1_7) {
							d.options[q++] = new Option(property_1_7[p][0], property_1_7[p][1]);
							p++;
						}
						break;
					}
					break;
				case "5":
					switch (flag) {
					case "0":
						var p = 0
							, q = 1;
						for (var j in property_1_0) {
							d.options[q++] = new Option(property_1_0[p][0], property_1_0[p][1]);
							p++;
						}
						break;
					}
					break;
				}
			}
		}
		var select_property_2 = function () {
			d.innerHTML = ""; //初始化
			d.style.display = "none";
			d.options[0] = new Option("请选择显示属性", "");
			var y_value = y.value
				, m_value = m.value;
			if (y_value == "" || m_value == "") {
				return;
			}
		}
		m.onchange = function () {
			var t_value = t.value;
			switch (t_value) {
			case "1":
				select_property_1();
				break;
			case "2":
				select_property_2();
				break;
			}
			//			select_property();
		}
		y.onchange = function () {
			select_file();
		}
		t.onchange = function () {
			var t_value = t.value;
			switch (t_value) {
			case "1":
				d.style.display = "block";
				break;
			case "2":
				d.innerHTML = "";
				d.style.display = "none";
				break;
			}
		}
	}
//	var selectTool=selectTool_init;
	if (typeof define === "function" && define.amd) {
		define(selectTool_init);
	}
	else if (typeof module === "object" && module.exports) {
		module.exports = selectTool_init;
	}
	else {
		this.selectTool = selectTool_init;
	}
})();