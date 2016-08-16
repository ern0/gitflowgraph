define([], function () {

	return function drawArrow(child, parent) {
		var rect1 = parent.getBoundingClientRect();
		var rect2 = child.getBoundingClientRect();

		var col1 = parent.getAttribute('data-column');
		var col2 = child.getAttribute('data-column');

		var w = Math.abs(rect1.left - rect2.left);
		var h = Math.abs(rect1.top - rect2.top + rect1.height);

		var arrow = document.createElement('div');
		arrow.className = 'arrow';

		if (col1 !== col2) {
			var deg = (Math.atan(w/h) / Math.PI * 180) * (col2 < col1 ? 1 : -1);
			arrow.style.height = Math.sqrt(Math.pow(h, 2) + Math.pow(w, 2)) + 'px';
			arrow.style.transform = 'rotate(' + deg + 'deg)';
		}
		else {
			arrow.style.height = h + 'px';
		}

		parent.appendChild(arrow);
	};

});