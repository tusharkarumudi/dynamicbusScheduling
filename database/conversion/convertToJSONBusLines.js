'use strict';

console.log("reading");
const fs = require('fs');

let rawdata = fs.readFileSync('FiveLinesWithStop.json');  
//let student = JSON.parse(rawdata);  
//console.log(student);  



  // Parse JSON string into object
    var input_JSON = JSON.parse(rawdata);



  var template_JSON = JSON.parse('{"bus_line_document": [{ "line_id": "", "bus_stops": [{ "_id":"","_name":"","longitude":"","latitude":""}]}]}');


	var busStopENTRY = template_JSON.bus_line_document[0].bus_stops[0];
	
	var emptyBusStopEntry = [];

	var emptyArray = [];

	var uniqueLineID = input_JSON[0].lineid;

	var i;
	
	for(i in input_JSON)
	{		
		if(uniqueLineID !== input_JSON[i].lineid)
		{

			//console.log("inside IF statement");
			//console.log(uniqueBusId +" "+ input_JSON[i].bus_vehicle_id);
	
			//save old data into array;
			template_JSON.bus_line_document[0].bus_stops = emptyBusStopEntry;					
			emptyBusStopEntry = [];
			emptyArray.push(template_JSON.bus_line_document[0]);				  			
			template_JSON = JSON.parse('{"bus_line_document": [{ "line_id": "", "bus_stops": [{ "_id":"", "name": "", "longitude" : "", "latitude": ""}]}]}');

			busStopENTRY = template_JSON.bus_line_document[0].bus_stops[0];			

		}


		uniqueLineID = input_JSON[i].lineid;

		template_JSON.bus_line_document[0].line_id = input_JSON[i].lineid;
		
		
		busStopENTRY._id = input_JSON[i].stopid;
		busStopENTRY._name = input_JSON[i].name;
		busStopENTRY.longitude = input_JSON[i].lon;		
		busStopENTRY.latitude = input_JSON[i].lat;		
		
		
		emptyBusStopEntry.push(busStopENTRY);

		busStopENTRY = JSON.parse('[{"bus_line_document": { "line_id": "", "bus_stops": [{ "_id":"", "name": "", "longitude" : "", "latitude": ""}]}}]')[0].bus_line_document.bus_stops[0];
		
	}

			template_JSON.bus_line_document[0].bus_stops = emptyBusStopEntry;			
			emptyBusStopEntry = [];
			emptyArray.push(template_JSON.bus_line_document[0]);		    
			
			//console.log(emptyArray);
console.log("Writing");
			
		    


 var result = JSON.parse('{"bus_line_document": [{ "line_id": "", "bus_stops": [{ "_id":"","_name":"","longitude":"","latitude":""}]}]}');
result.bus_line_document = emptyArray;
		let writeData = JSON.stringify(result);
		fs.writeFileSync('FiveLinesWithStopOutput.json', writeData);  
