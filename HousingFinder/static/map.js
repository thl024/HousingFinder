// Constants
let ACCESS_TOKEN = 'pk.eyJ1IjoidGhsMDI0IiwiYSI6ImNqZng3MjZkdDRrem4ycXFvcWR3ZDJpZmIifQ.OGbnzl419bgjSwteuia3Eg'
let ATTRIBUTION = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>'

// Variables
var map;

// Start function
$(function () {

	// Instantiate map
	map = L.map('map').setView([32.5149, -117.0382], 12);

	// Load access token
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    	attribution: ATTRIBUTION,
    	maxZoom: 18,
    	id: 'mapbox.streets',
    	accessToken: ACCESS_TOKEN
	}).addTo(map);
})