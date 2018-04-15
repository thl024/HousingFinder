// Constants
let ACCESS_TOKEN = 'pk.eyJ1IjoidGhsMDI0IiwiYSI6ImNqZng3MjZkdDRrem4ycXFvcWR3ZDJpZmIifQ.OGbnzl419bgjSwteuia3Eg';
let ATTRIBUTION = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>';
// TODO CHANGE
let API_BASE_URL = 'http://localhost:8000/api/'
let INITIAL_CENTER = [32.861196, -117.174040]

// Variables
var map;
var apartments;

// Extend icons
var ApartmentIcon = L.Icon.extend({
	options: {
        iconUrl: ambulanceIconURL,
        iconSize: new L.Point(24, 24),
        popupAnchor: new L.Point(0, -24)
	}
});

// Start function
$(function () {

	// Instantiate map
	map = L.map('map').setView(INITIAL_CENTER, 12);

	// Load access token
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    	attribution: ATTRIBUTION,
    	maxZoom: 18,
    	id: 'mapbox.streets',
    	accessToken: ACCESS_TOKEN
	}).addTo(map);

	// AJAX Call to get all apartments
	getApartments()

})

function getApartments() {
	$.ajax({
		type: 'GET',
		datatype: 'json',
		url: API_BASE_URL + 'apartments',

		error: function (msg) {
			console.log(msg);
		},

		success: function (data) {
			renderApartments(data);
		},
	})
}

function renderApartments(data) {
	apartments = data;

	$.each(apartments, function(index, apartment) {
		var aptIcon = new ApartmentIcon()
        var aptMarker = L.marker(
            [apartment.latitude, apartment.longitude],
            {
                icon: aptIcon,
            }
        ).bindPopup(
            "<b>Name: </b>" + apartment.name +
            "<br/>" +
            "<b>Address: </b>" + apartment.address +
            "<br/>" + 
            "<b>Rent Price: </b>$" + apartment.rent_price +
            "<br/>" + 
            "<b>Bedrooms: </b>" + apartment.bedrooms +
            '<br/>' + 
            "<b>Bathrooms: </b>" + apartment.bathrooms + 
            '<br/>' + 
            "<b>Size: </b>" + apartment.size + " ft squared"
        ).addTo(map)
	})
}