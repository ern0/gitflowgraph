define([
		'mustache', 
		'underscore',
		'text!templates/tree.mustache',
		'csshelpers',
		'arrow'
	], function (Mustache, _, treeTmpl, css, drawArrow) {

	var getBadge = function (node) {
		return node.querySelector('.git-node-badge');
	};

	var getDataNode = function (node) {
		return node.querySelector('.git-node-data');
	};

	var processArrow = function (node, attr, className) {
		var parent = node.getAttribute(attr);
		var parentElem = parent && document.getElementById(parent);
		if (parentElem) drawArrow(getBadge(node), getBadge(parentElem), className);
	};

	var setPositions = function (domElement, columns) {
		var nodes = domElement.querySelectorAll('.git-node');
		var badge = getBadge(nodes[0]);
		var data = getDataNode(nodes[0]);

		var badgeWidth = css.getWidth(badge);

		var boxWidth = css.getWidth(nodes[0]);
		var boxPaddingLeft = css.getInt(nodes[0], 'paddingLeft');
		var boxPaddingRight = css.getInt(nodes[0], 'paddingRight');
		var boxCanvasWidth = boxWidth - boxPaddingLeft - boxPaddingRight;
		var dataMaxWidth = css.getFromPercent(css.getInt(data, 'maxWidth'), boxCanvasWidth);
		var boxUsableWidth = boxCanvasWidth - dataMaxWidth;

		var margin = (boxUsableWidth - (columns * badgeWidth)) / (columns - 1);

		_(nodes).each(function (node) {
			var column = node.getAttribute('data-column');

			var d = css.getPercent(column * (badgeWidth + margin), boxCanvasWidth);
			css.set(getBadge(node), 'marginLeft', d);

			processArrow(node, 'data-parent', '');
			processArrow(node, 'data-parent2', 'merge');
		});

		for (var i = 0; i < columns; i++) {
			var sep = document.createElement('li');
			sep.className = 'column-indicator';
			css.set(sep, 'left', css.getPercent(i * (badgeWidth + margin), boxWidth));
			domElement.querySelector('.git-tree').appendChild(sep);
		}
	};

	return function draw(domElement, data, options) {

		_(data).extend({
			timestampRFC3339: function () {
				return this.replace(' ', 'T') + 'Z';
			},
			shortenHash: function () {
				return this.substr(0, 6);
			}
		});

		domElement.innerHTML = Mustache.render(treeTmpl, data);
		
		setPositions(domElement, data.meta.columns);

		document.querySelector('.switch-view').addEventListener('click', function () {
			document.querySelector('.git-repo').classList.toggle('sideview');
		});
	};

});