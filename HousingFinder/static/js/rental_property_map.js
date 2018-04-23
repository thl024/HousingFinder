// Constants
let ACCESS_TOKEN = 'pk.eyJ1IjoidGhsMDI0IiwiYSI6ImNqZng3MjZkdDRrem4ycXFvcWR3ZDJpZmIifQ.OGbnzl419bgjSwteuia3Eg';
let ATTRIBUTION = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>';
// TODO CHANGE
let API_BASE_URL = 'http://localhost:8000/api/'
let INITIAL_CENTER = [32.861196, -117.174040]

// Variables
var map;

// Extend icons
var RentalIcon = L.Icon.extend({
	options: {
        iconUrl: rentalIconURL,
        iconSize: new L.Point(24, 24),
        popupAnchor: new L.Point(0, -18)
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

	renderRentals()

})

function renderRentals() {
	$.each(rentals, function(index, rental) {
		var rntIcon = new RentalIcon()
        var rntMarker = L.marker([rental.latitude, rental.longitude],
            {
                icon: rntIcon,
            }
        ).bindPopup(
            "<b>Name: </b>" + rental.name +
            "<br/>" +
            "<b>Address: </b>" + rental.address +
            "<br/>" + 
            "<b>Rent Price: </b>$" + rental.rent_price +
            "<br/>" + 
            "<b>Bedrooms: </b>" + rental.bedrooms +
            '<br/>' + 
            "<b>Bathrooms: </b>" + rental.bathrooms + 
            '<br/>' + 
            "<b>Size: </b>" + rental.size + " ft squared"
        ).on('mouseover', function(e) {
            this.openPopup();
        }).on('mouseout', function(e) {
            this.closePopup();
        }).on('click', function(e) {
            window.open(rental.listing_url);
        }).addTo(map)
	})
}