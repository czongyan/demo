! function () {
	var show = {
		version: "1.1.1"
	};
	var f = document.getElementById("interval")
		, s = document.getElementById("file")
		, t = document.getElementById("map");
	//年
	var interval = new Date().getFullYear();
	for (var i = year; i >= 1990; i--) {
		y.options[year + 1 - i] = new Option(i, i); //第一个参数是option的文本值，第二个参数是option的value值
	}
	//月
	for (var i = 1; i <= 12; i++) {
		m.options[i] = new Option(i, i);
	}
	//日
	var day = function () {
		d.length = 1; //初始化
		var y_value = y.value
			, m_value = m.value;
		if (y_value == "" || m_value == "") {
			return;
		}
		else {
			var arr = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
			if ((y_value % 4 == 0 && y_value % 100 != 0) || y_value % 400 == 0) {
				arr[1]++;
			}
			for (i = 1; i <= arr[m_value - 1]; i++) {
				d.options[i] = new Option(i, i);
			}
		}
	}
	y.onchange = function () {
		day();
	}
	m.onchange = function () {
		day();
	}
	var fileName = function () {}
	if (typeof define === "function" && define.amd) {
		define(d3);
	}
	else if (typeof module === "object" && module.exports) {
		module.exports = d3;
	}
	else {
		this.d3 = d3;
	}
}();


mo.svg.brush = function () {
		function n(i) {
			i.each(function () {
				var i = mo.select(this).style("pointer-events", "all").style("-webkit-tap-highlight-color", "rgba(0,0,0,0)").on("mousedown.brush", u).on("touchstart.brush", u)
					, o = i.selectAll(".background").data([0]);
				o.enter().append("rect").attr("class", "background").style("visibility", "hidden").style("cursor", "crosshair"), i.selectAll(".extent").data([0]).enter().append("rect").attr("class", "extent").style("cursor", "move");
				var a = i.selectAll(".resize").data(v, dt);
				a.exit().remove(), a.enter().append("g").attr("class", function (n) {
					return "resize " + n
				}).style("cursor", function (n) {
					return Xc[n]
				}).append("rect").attr("x", function (n) {
					return /[ew]$/.test(n) ? -3 : null
				}).attr("y", function (n) {
					return /^[ns]/.test(n) ? -3 : null
				}).attr("width", 6).attr("height", 6).style("visibility", "hidden"), a.style("display", n.empty() ? "none" : null);
				var s, f = mo.transition(i)
					, h = mo.transition(o);
				c && (s = Bu(c), h.attr("x", s[0]).attr("width", s[1] - s[0]), e(f)), l && (s = Bu(l), h.attr("y", s[0]).attr("height", s[1] - s[0]), r(f)), t(f)
			})
		}

		function t(n) {
			n.selectAll(".resize").attr("transform", function (n) {
				return "translate(" + s[+/e$/.test(n)] + "," + h[+/^s/.test(n)] + ")"
			})
		}

		function e(n) {
			n.select(".extent").attr("x", s[0]), n.selectAll(".extent,.n>rect,.s>rect").attr("width", s[1] - s[0])
		}

		function r(n) {
			n.select(".extent").attr("y", h[0]), n.selectAll(".extent,.e>rect,.w>rect").attr("height", h[1] - h[0])
		}

		function u() {
			function u() {
				32 == mo.event.keyCode && (N || (M = null, q[0] -= s[1], q[1] -= h[1], N = 2), f())
			}

			function g() {
				32 == mo.event.keyCode && 2 == N && (q[0] += s[1], q[1] += h[1], N = 0, f())
			}

			function v() {
				var n = mo.mouse(b)
					, u = !1;
				x && (n[0] += x[0], n[1] += x[1]), N || (mo.event.altKey ? (M || (M = [(s[0] + s[1]) / 2, (h[0] + h[1]) / 2]), q[0] = s[+(n[0] < M[0])], q[1] = h[+(n[1] < M[1])]) : M = null), k && m(n, c, 0) && (e(S), u = !0), A && m(n, l, 1) && (r(S), u = !0), u && (t(S), w({
					type: "brush"
					, mode: N ? "move" : "resize"
				}))
			}

			function m(n, t, e) {
				var r, u, a = Bu(t)
					, c = a[0]
					, l = a[1]
					, f = q[e]
					, g = e ? h : s
					, v = g[1] - g[0];
				return N && (c -= f, l -= v + f), r = (e ? d : p) ? Math.max(c, Math.min(l, n[e])) : n[e], N ? u = (r += f) + v : (M && (f = Math.max(c, Math.min(l, 2 * M[e] - r))), r > f ? (u = r, r = f) : u = f), g[0] != r || g[1] != u ? (e ? o = null : i = null, g[0] = r, g[1] = u, !0) : void 0
			}

			function y() {
				v(), S.style("pointer-events", "all").selectAll(".resize").style("display", n.empty() ? "none" : null), mo.select("body").style("cursor", null), z.on("mousemove.brush", null).on("mouseup.brush", null).on("touchmove.brush", null).on("touchend.brush", null).on("keydown.brush", null).on("keyup.brush", null), T(), w({
					type: "brushend"
				})
			}
			var M, x, b = this
				, _ = mo.select(mo.event.target)
				, w = a.of(b, arguments)
				, S = mo.select(b)
				, E = _.datum()
				, k = !/^(n|s)$/.test(E) && c
				, A = !/^(e|w)$/.test(E) && l
				, N = _.classed("extent")
				, T = L()
				, q = mo.mouse(b)
				, z = mo.select(_o).on("keydown.brush", u).on("keyup.brush", g);
			if (mo.event.changedTouches ? z.on("touchmove.brush", v).on("touchend.brush", y) : z.on("mousemove.brush", v).on("mouseup.brush", y), S.interrupt().selectAll("*").interrupt(), N) q[0] = s[0] - q[0], q[1] = h[0] - q[1];
			else if (E) {
				var C = +/w$/.test(E)
					, D = +/^n/.test(E);
				x = [s[1 - C] - q[0], h[1 - D] - q[1]], q[0] = s[C], q[1] = h[D]
			}
			else mo.event.altKey && (M = q.slice());
			S.style("pointer-events", "none").selectAll(".resize").style("display", null), mo.select("body").style("cursor", _.style("cursor")), w({
				type: "brushstart"
			}), v()
		}
		var i, o, a = g(n, "brushstart", "brush", "brushend")
			, c = null
			, l = null
			, s = [0, 0]
			, h = [0, 0]
			, p = !0
			, d = !0
			, v = $c[0];
		return n.event = function (n) {
			n.each(function () {
				var n = a.of(this, arguments)
					, t = {
						x: s
						, y: h
						, i: i
						, j: o
					}
					, e = this.__chart__ || t;
				this.__chart__ = t, Pc ? mo.select(this).transition().each("start.brush", function () {
					i = e.i, o = e.j, s = e.x, h = e.y, n({
						type: "brushstart"
					})
				}).tween("brush:brush", function () {
					var e = kr(s, t.x)
						, r = kr(h, t.y);
					return i = o = null
						, function (u) {
							s = t.x = e(u), h = t.y = r(u), n({
								type: "brush"
								, mode: "resize"
							})
						}
				}).each("end.brush", function () {
					i = t.i, o = t.j, n({
						type: "brush"
						, mode: "resize"
					}), n({
						type: "brushend"
					})
				}) : (n({
					type: "brushstart"
				}), n({
					type: "brush"
					, mode: "resize"
				}), n({
					type: "brushend"
				}))
			})
		}, n.x = function (t) {
			return arguments.length ? (c = t, v = $c[!c << 1 | !l], n) : c
		}, n.y = function (t) {
			return arguments.length ? (l = t, v = $c[!c << 1 | !l], n) : l
		}, n.clamp = function (t) {
			return arguments.length ? (c && l ? (p = !!t[0], d = !!t[1]) : c ? p = !!t : l && (d = !!t), n) : c && l ? [p, d] : c ? p : l ? d : null
		}, n.extent = function (t) {
			var e, r, u, a, f;
			return arguments.length ? (c && (e = t[0], r = t[1], l && (e = e[0], r = r[0]), i = [e, r], c.invert && (e = c(e), r = c(r)), e > r && (f = e, e = r, r = f), (e != s[0] || r != s[1]) && (s = [e, r])), l && (u = t[0], a = t[1], c && (u = u[1], a = a[1]), o = [u, a], l.invert && (u = l(u), a = l(a)), u > a && (f = u, u = a, a = f), (u != h[0] || a != h[1]) && (h = [u, a])), n) : (c && (i ? (e = i[0], r = i[1]) : (e = s[0], r = s[1], c.invert && (e = c.invert(e), r = c.invert(r)), e > r && (f = e, e = r, r = f))), l && (o ? (u = o[0], a = o[1]) : (u = h[0], a = h[1], l.invert && (u = l.invert(u), a = l.invert(a)), u > a && (f = u, u = a, a = f))), c && l ? [[e, u], [r, a]] : c ? [e, r] : l && [u, a])
		}, n.clear = function () {
			return n.empty() || (s = [0, 0], h = [0, 0], i = o = null), n
		}, n.empty = function () {
			return !!c && s[0] == s[1] || !!l && h[0] == h[1]
		}, mo.rebind(n, a, "on")
	};