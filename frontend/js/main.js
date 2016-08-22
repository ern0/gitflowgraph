require(['loadJSON', 'draw'], function (loadJSON, draw) {

	loadJSON('/fetch', function (data) {
		draw(document.getElementById('drawhere'), data, {});
	});

});