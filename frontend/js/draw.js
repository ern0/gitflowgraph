define([
		'mustache', 
		'underscore',
		'text!templates/tree.mustache',
		'arrow'
	], function (Mustache, _, treeTmpl, drawArrow) {

	return function draw(domElement, data, options) {

		var mustacheVars = {
			nodes: data
		};

		domElement.innerHTML = Mustache.render(treeTmpl, mustacheVars);

		_(domElement.querySelectorAll('.git-node')).each(function (node) {
			var column = node.getAttribute('data-column');
			var w = node.getBoundingClientRect().width;
			var margin = parseInt(window.getComputedStyle(node).marginLeft, 10);
			node.style.left = ((column - 1) * (w + margin)) + 'px';

			var parent = node.getAttribute('data-parent');
			if (parent) {
				drawArrow(node, document.getElementById(parent));
			}
		});

	};

});