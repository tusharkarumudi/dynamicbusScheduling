'use strict';

console.log("reading");
const fs = require('fs');

let rawdata = fs.readFileSync('tp.json');  
//let student = JSON.parse(rawdata);  
//console.log(student);  



  // Parse JSON string into object
    var input_JSON = JSON.parse(rawdata);



  var template_JSON =	JSON.parse('{ "timetable_document": [{ "id": "", "lineid": "","bus_vehicle_id": "", "timetableid": "","timetable_entries": [{"starting_bus_stop":{"startingid": "","startingpointname": "","startlat": "","startlon": ""},"ending_bus_stop": {"endingpointid": "","endingpointname": "","endingpointlat": "","endingpointlong": ""},"departure_datetime":"","arrival_datetime":"","total_time":"","numberofonboarding": "","numberofdeboarding": "","numberofcurrent": ""}]}]}');


	var ENTRY = template_JSON.timetable_document[0].timetable_entries[0];
	
	var emptyEntry = [];

	var emptyArray = [];
	
	
	var entryIndex = 0
	var uniqueBusId = input_JSON[0].bus_vehicle_id;
	var i;
	
	for(i in input_JSON)
	{		
		if(uniqueBusId !== input_JSON[i].bus_vehicle_id)
		{

			//console.log("inside IF statement");
			//console.log(uniqueBusId +" "+ input_JSON[i].bus_vehicle_id);
	
			//save old data into array;
			template_JSON.timetable_document[0].timetable_entries = emptyEntry;					
			emptyEntry = [];
			emptyArray.push(template_JSON.timetable_document[0]);				  			
			template_JSON = JSON.parse('{ "timetable_document": [{ "id": "", "lineid": "","bus_vehicle_id": "", "timetableid": "","timetable_entries": [{"starting_bus_stop":{"startingid": "","startingpointname": "","startlat": "","startlon": ""},"ending_bus_stop": {"endingpointid": "","endingpointname": "","endingpointlat": "","endingpointlong": ""},"departure_datetime":"","arrival_datetime":"","total_time":"","numberofonboarding": "","numberofdeboarding": "","numberofcurrent": ""}]}]}');	

ENTRY = template_JSON.timetable_document[0].timetable_entries[0];			

		}


		uniqueBusId = input_JSON[i].bus_vehicle_id;

		template_JSON.timetable_document[0].bus_vehicle_id = input_JSON[i].bus_vehicle_id;
		template_JSON.timetable_document[0].lineid = input_JSON[i].line_id;
		template_JSON.timetable_document[0].timetableid = input_JSON[i].timetable_id;
		
		ENTRY.numberofcurrent = input_JSON[i].number_of_current_passengers;
		ENTRY.numberofdeboarding = input_JSON[i].number_of_deboarding_passengers;
		ENTRY.numberofonboarding = input_JSON[i].number_of_onboarding_passengers;
		
		ENTRY.departure_datetime = input_JSON[i].departure_datetime;
		ENTRY.arrival_datetime = input_JSON[i].arrival_datetime;
		ENTRY.total_time = input_JSON[i].total_time;
		
		ENTRY.starting_bus_stop.startingid = input_JSON[i].starting_bus_stop_id;
		ENTRY.starting_bus_stop.startingpointname = input_JSON[i].starting_bus_stop_name;
		ENTRY.starting_bus_stop.startlat = input_JSON[i].starting_bus_stop_point_lat;
		ENTRY.starting_bus_stop.startlon = input_JSON[i].starting_bus_stop_point_long;
		
		ENTRY.ending_bus_stop.endingpointid = input_JSON[i].ending_bus_stop_id;
		ENTRY.ending_bus_stop.endingpointname = input_JSON[i].ending_bus_stop_name;
		ENTRY.ending_bus_stop.endingpointlat = input_JSON[i].ending_bus_stop_point_lat;
		ENTRY.ending_bus_stop.endingpointlong = input_JSON[i].ending_bus_stop_point_long;

		emptyEntry.push(ENTRY);

//whatever		
		ENTRY = JSON.parse('{ "timetable_document": [{ "id": "", "lineid": "","bus_vehicle_id": "", "timetableid": "","timetable_entries": [{"starting_bus_stop":{"startingid": "","startingpointname": "","startlat": "","startlon": ""},"ending_bus_stop": {"endingpointid": "","endingpointname": "","endingpointlat": "","endingpointlong": ""},"departure_datetime":"","arrival_datetime":"","total_time":"","numberofonboarding": "","numberofdeboarding": "","numberofcurrent": ""}]}]}').timetable_document[0].timetable_entries[0];
		
	}

			template_JSON.timetable_document[0].timetable_entries = emptyEntry;					
			emptyEntry = [];
			emptyArray.push(template_JSON.timetable_document[0]);		    
			
			//console.log(emptyArray);
console.log("Writing");
			
		    

 var result = JSON.parse('{ "timetable_document": [{ "id": "", "lineid": "","bus_vehicle_id": "", "timetableid": "","timetable_entries": [{"starting_bus_stop":{"startingid": "","startingpointname": "","startlat": "","startlon": ""},"ending_bus_stop": {"endingpointid": "","endingpointname": "","endingpointlat": "","endingpointlong": ""},"departure_datetime":"","arrival_datetime":"","total_time":"","numberofonboarding": "","numberofdeboarding": "","numberofcurrent": ""}]}]}');
result.timetable_document = emptyArray;


		let writeData = JSON.stringify(result);
		fs.writeFileSync('tpTimeTableOutput.json', writeData);  
