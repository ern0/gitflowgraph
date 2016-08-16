module.exports = function(grunt) {

	require('load-grunt-tasks')(grunt, {
		scope: 'devDependencies'
	});

	var config = {
		pkg: grunt.file.readJSON('bower.json')
	};

	grunt.util._.extend(config, loadConfig('./grunt-tasks/options/'));
 	grunt.initConfig(config);

	grunt.registerTask('default', [
		'jshint',
		'clean:dist',
		'requirejs'
	]);

	grunt.registerTask('setup', [
		'clean:jslib',
		'bower'
	]);

	function loadConfig(path) {
		var glob = require('glob');
		var object = {};
		var key;

		glob.sync('*', {cwd: path}).forEach(function(option) {
			key = option.replace(/\.js$/,'');
			object[key] = require(path + option);
		});

		return object;
	}

};
