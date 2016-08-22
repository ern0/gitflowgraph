define(['csshelpers'], function (css) {

	return function drawArrow(child, parent, className) {
		var rect1 = parent.getBoundingClientRect();
		var rect2 = child.getBoundingClientRect();

		var w = Math.abs(rect1.left - rect2.left);
		var h = Math.abs(rect1.top - rect2.top + rect1.height);

		var arrow = document.createElement('div');
		arrow.className = 'arrow ' + className;

		var deg = (Math.atan(w/h) / Math.PI * 180) * (rect2.left < rect1.left ? 1 : -1);
		arrow.style.height = Math.sqrt(Math.pow(h, 2) + Math.pow(w, 2)) + 'px';
		arrow.style.transform = 'rotate(' + deg + 'deg)';

		parent.appendChild(arrow);
	};

});