var express = require('express');
var router = express.Router();
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
const Alexa = require('ask-sdk-core')

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Bus Scheduling' });
});

// use 'ask-sdk' if standard SDK module is installed
////////////////////////////////
// Code for the handlers here //
////////////////////////////////

// const LaunchRequestHandler = {
//     canHandle(handlerInput) {
//         return handlerInput.requestEnvelope.request.type === 'LaunchRequest';
//     },
//     handle(handlerInput) {
//         const speechText = 'Welcome to Nashville MTA';
//         return handlerInput.responseBuilder
//             .speak(speechText)
//             .reprompt(speechText)
//             .withSimpleCard('Welcome to Nashville MTA', speechText)
//             .getResponse();
//     }
// };
// const BusToIntentHandler = {
//
//     canHandle(handlerInput) {
//         return handlerInput.requestEnvelope.request.type === 'IntentRequest'
//             && handlerInput.requestEnvelope.request.intent.name === 'BusTo' ;
//     },
//     handle(handlerInput) {
//         return handlebusRequest(handlerInput);
//         /* return handlerInput.responseBuilder
//              .speak(speechText)
//              .withSimpleCard('Hello Tushar', speechText)
//              .getResponse();*/
//     }
// };
// const HelpIntentHandler = {
//     canHandle(handlerInput) {
//         return handlerInput.requestEnvelope.request.type === 'IntentRequest'
//             && handlerInput.requestEnvelope.request.intent.name === 'AMAZON.HelpIntent';
//     },
//     handle(handlerInput) {
//         const speechText = 'You can put requests for a bus';
//         return handlerInput.responseBuilder
//             .speak(speechText)
//             .reprompt(speechText)
//             .withSimpleCard('Bus from x to y', speechText)
//             .getResponse();
//     }
// };
// const CancelAndStopIntentHandler = {
//     canHandle(handlerInput) {
//         return handlerInput.requestEnvelope.request.type === 'IntentRequest'
//             && (handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent'
//                 || handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent');
//     },
//     handle(handlerInput) {
//         const speechText = 'Goodbye!';
//         return handlerInput.responseBuilder
//             .speak(speechText)
//             .withSimpleCard('Good bye', speechText)
//             .getResponse();
//     }
// };
// const SessionEndedRequestHandler = {
//     canHandle(handlerInput) {
//         return handlerInput.requestEnvelope.request.type === 'SessionEndedRequest';
//     },
//     handle(handlerInput) {
//         //any cleanup logic goes here
//         return handlerInput.responseBuilder.getResponse();
//     }
// };
// const ErrorHandler = {
//     canHandle() {
//         return true;
//     },
//     handle(handlerInput, error) {
//         console.log(`Error handled: ${error.message}`);
//         return handlerInput.responseBuilder
//             .speak('Sorry, I can\'t understand the command. Please say again.')
//             .reprompt('Sorry, I can\'t understand the command. Please say again.')
//             .getResponse();
//     },
// };
//
// function handlebusRequest(handlerInput){
//     const speechText = 'Your Request has been accepted';
//     const { requestEnvelope, attributesManager, responseBuilder } = handlerInput;
//     const { intent } = requestEnvelope.request;
//     console.log("Starting point: "+ intent.slots.Startingpoint.value);
//     var dateTime = require('node-datetime');
//     var dt = dateTime.create();
//     var formatted = dt.format('H:M:S');
//     console.log(formatted);
//     var MongoClient = require('mongodb').MongoClient;
//     MongoClient.connect("mongodb://localhost:27017/MyDb", function (err, db) {
//         db.collection('travelRequest', function (err, collection) {
//             collection.insert({ clientId: 1, lineId: 'Steve', startingbusstopname: 'Jobs', });
//
//         });
//     });
//
//     return handlerInput.responseBuilder
//         .speak(speechText)
//         .getResponse();
// }
//
// exports.handler = Alexa.SkillBuilders.custom()
//     .addRequestHandlers(LaunchRequestHandler,
//         BusToIntentHandler,
//         HelpIntentHandler,
//         CancelAndStopIntentHandler,
//         SessionEndedRequestHandler).lambda();

var BusStop, timetablecollectiondata;
// Connection URL
const url = 'mongodb://localhost:27017';

// Database Name
const dbName = 'Dynamic_Bus_Scheduling';

MongoClient.connect(url, function(err, client) {

    //create empty array of waiting times
    //call travel request get all data

    //for each travel request
        //take its departure time and bus stop
        //get arrival times of that bus stop from Timetable
        //calculate minimum waiting time
        //push minimum waiting time into array.

    //calculate mean of waiting times.
    //compare this mean with the threshold.

    //Connecting to Timetable document
    const col = client.db(dbName).collection('Timetable');
    // Show that duplicate records got dropped
    col.find().toArray(function(err, items) {
        assert.equal(null, err);
        timetablecollectiondata = items
    });

    //Connecting to TravelRequest Documents
    const trd = client.db(dbName).collection('TravelRequestDocuments');
    trd.find().toArray(function (err, items) {
        //console.log(items[0])
        var totalNumberOfRequests= items[0]["travel_request_document"].length;
        var totalWaitingTime = 0;
        for(i in items[0]["travel_request_document"]){

            var RequestedArrivingTime = items[0]["travel_request_document"][i].departure_datetime;
            BusStop = (items[0]["travel_request_document"][i].starting_bus_stop.stopid)
            BusStop = "100OAKS"
            var ArrivingTimes = GetArrivingTimes(BusStop)
            //console.log(items[0]["travel_request_document"][i].departure_datetime)
            console.log("minimum time of minimum")
            //console.log(ArrivingTimes)
            var minimumTime = GetMinimumWaitingTimeForTravelRequest(RequestedArrivingTime, ArrivingTimes)
            // console.log(minimumTime)
            totalWaitingTime = totalWaitingTime+minimumTime;
        }
        client.close();
        var AverageWaitingTime = totalWaitingTime/totalNumberOfRequests;
        console.log(AverageWaitingTime);
        if(AverageWaitingTime >= 1500) {
            console.log("scheduling a bus");
            //dynamicBusData("9","30");
        }
        else {
            console.log("Bus is not Scheduled")
            dynamicBusData("9","30");
        }
    })
});

function GetArrivingTimes(busStop) {
    for(i in timetablecollectiondata[0]["timetable"]) {
        //console.log("printing next");

        //console.log(i)
        //    console.log(items[0][i])
        //console.log(items[0]["timetable"][i].busstop);
        if(timetablecollectiondata[0]["timetable"][i].busstop == busStop) {
            arr_array = timetablecollectiondata[0]["timetable"][i].arr_time;
            break
            //console.log(arr_array[1])
        }
    }
    return arr_array;
}

function GetMinimumWaitingTimeForTravelRequest(RequestedArrivingTime, ArrivingTimes)
{
    // var RequestedArrivingTime = "6:16:00";
    // var ArrivingTimes = ["07:00",
    //     "08:00:00",
    //     "09:00:00",
    //     "10:00:00",
    //     "11:00:00",
    //     "12:00:00",
    //     "13:00",
    //     "14:00",
    //     "15:00",
    //     "16:00",
    //     "17:00",
    //     "18:00"
    // ];

    var RequestedArrivingTimeInSeconds = GetSecondsFromTime(RequestedArrivingTime);
    var WaitingTimes = [];

    for(var arrivingTime in ArrivingTimes)
    {
        var ArrivingTimesInSeconds = GetSecondsFromTime(ArrivingTimes[arrivingTime]);
        WaitingTimes.push(Math.abs(ArrivingTimesInSeconds-RequestedArrivingTimeInSeconds));
    }
    var MinimumWaitingTime = FindMinimumWaitingTimes(WaitingTimes);
    return MinimumWaitingTime;
}

function GetSecondsFromTime(TimeInString)
{
    var hours = TimeInString.split(":")[0];
    var minutes = TimeInString.split(":")[1];
    var seconds = (hours*60*60)+(minutes*60);
    return seconds;
}

function FindMinimumWaitingTimes(WaitingTimes)
{
    var minimum = WaitingTimes[0];

    for(var time in WaitingTimes)
    {
        if(WaitingTimes[time]<minimum)
        {
            minimum = WaitingTimes[time];
        }
    }
    return minimum;
}

function dynamicBusData(NewStartHour, NewStartMinute){
    var NewStartHour = "9";
    var NewStartMinute = "30"
    //var stopArray = ["100OAKS", "5AVGAYNN", "6AOAKSN", "6THLAFNN", "7AVCHUSN", "7AVCOMSN", "7AVUNISM", "8ABRONM", "8ABRONN", "8ABROSN"]
    var timeDiff = ["0", "15", "5", "5", "5", "5", "10", "11", "4", "15"]
    var template = [
        {
            "LineID": "100OAKS",
            "CountOfBuses": "1",
            "route": ["100OAKS", "5AVGAYNN", "6AOAKSN", "6THLAFNN", "7AVCHUSN", "7AVCOMSN", "7AVUNISM", "8ABRONM", "8ABRONN", "8ABROSN"],
            "NewArrivingTimes":["9.30"]
        }
    ];

    var NewArrivingTimes = [];

    for(var i in timeDiff)
    {
        NewStartMinute = parseInt(timeDiff[i]) + parseInt(NewStartMinute);
        // console.log(timeDiff[i]);
        // console.log(NewStartMinute);
        //console.log(NewStartMinute);
        if(NewStartMinute < 60)
        {
            NewArrivingTimes.push(NewStartHour+":"+NewStartMinute);
        }
        else
        {
            var hh = parseInt(parseInt((NewStartMinute)/60)+parseInt(NewStartHour));
            var mm = parseInt(parseInt(NewStartMinute)%60);
            NewArrivingTimes.push(hh+":"+mm);
        }

    }
    //console.log(NewArrivingTimes);
    template[0].NewArrivingTimes = NewArrivingTimes;
    console.log("template is:");
    console.log(template);
    //console.log(template);
    MongoClient.connect(url, function(err, client){
        const dbd = client.db(dbName).collection('DynamicBusData');
        dbd.insertMany(template, function (err, res) {
            if (err) throw err;
            console.log("Number of documents inserted: " + res.insertedCount);
            client.close()
        });
    });
}

module.exports = router;
