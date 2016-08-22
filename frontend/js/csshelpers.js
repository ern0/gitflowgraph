define([], function () {

	return {
		get: function (node, property) {
			return window.getComputedStyle(node)[property];
		},

		getInt: function (node, property) {
			return parseInt(this.get(node, property), 10);
		},

		set: function (node, property, value) {
			node.style[property] = value;
		},

		getPercent: function (value, fullValue) {
			return value / fullValue * 100 + '%';
		},

		getFromPercent: function (percent, fullValue) {
			return percent * fullValue / 100;
		},

		getWidth: function (node) {
			return node.getBoundingClientRect().width;
		}
	};

});