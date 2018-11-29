var express = require('express');
var router = express.Router();
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
const Alexa = require('ask-sdk-core')

// Connection URL
const url = 'mongodb://localhost:27017';

// Database Name
const dbName = 'Dynamic_Bus_Scheduling';

/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index', { title: 'Nashville Metropolitan Transit Authority' });
});

router.get('/timetable', function(req, res, next) {
    MongoClient.connect(url, function(err, client) {

        //Connecting to Timetable document
        var col = client.db(dbName).collection('Timetable');
        col.find().toArray(function(err, items) {
            res.render('timetable', { title: 'Nashville Metropolitan Transit Authority', timetable: items});
        });
        client.close();
        });
});

router.get('/travelrequest', function(req, res, next) {
    MongoClient.connect(url, function(err, client) {

        //Connecting to Timetable document
        var trd = client.db(dbName).collection('TravelRequestDocuments');
        trd.find().toArray(function(err, items) {
            res.render('travelrequest', { title: 'Nashville Metropolitan Transit Authority', travelrequest: items});
        });
        client.close();
    });
});

router.get('/dynamicbusdata', function(req, res, next) {
    MongoClient.connect(url, function(err, client) {

        //Connecting to Timetable document
        var dbd = client.db(dbName).collection('DynamicBusData');
        dbd.find().toArray(function(err, items) {
            res.render('dynamicbusdata', { title: 'Nashville Metropolitan Transit Authority', dynamicbusdata: items});
        });
        client.close();
    });
});

/*
//Alexa code starts here
let skill;

const LaunchRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'LaunchRequest';
    },
    handle(handlerInput) {
        const speechText = 'Welcome to Nashville MTA';
        return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt(speechText)
            .withSimpleCard('Welcome to Nashville MTA', speechText)
            .getResponse();
    }
};
const BusToIntentHandler = {

    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'BusTo' ;
    },
    handle(handlerInput) {
        return handlebusRequest(handlerInput);
    }
};
const HelpIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'AMAZON.HelpIntent';
    },
    handle(handlerInput) {
        const speechText = 'You can put requests for a bus';
        return handlerInput.responseBuilder
            .speak(speechText)
            .reprompt(speechText)
            .withSimpleCard('Bus from x to y', speechText)
            .getResponse();
    }
};
const CancelAndStopIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && (handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent'
                || handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent');
    },
    handle(handlerInput) {
        const speechText = 'Goodbye!';
        return handlerInput.responseBuilder
            .speak(speechText)
            .withSimpleCard('Good bye', speechText)
            .getResponse();
    }
};
const SessionEndedRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'SessionEndedRequest';
    },
    handle(handlerInput) {
        //any cleanup logic goes here
        return handlerInput.responseBuilder.getResponse();
    }
};
const ErrorHandler = {
    canHandle() {
        return true;
    },
    handle(handlerInput, error) {
        console.log(`Error handled: ${error.message}`);
        return handlerInput.responseBuilder
            .speak('Sorry, I can\'t understand the command. Please say again.')
            .reprompt('Sorry, I can\'t understand the command. Please say again.')
            .getResponse();
    },
};

function handlebusRequest(handlerInput) {
    const speechText = 'Your Request has been accepted';
    const {requestEnvelope, attributesManager, responseBuilder} = handlerInput;
    const {intent} = requestEnvelope.request;
    var dateTime = require('node-datetime');
    var dt = dateTime.create();
    var formatted = dt.format('H:M:S');
    //console.log("starting value "+intent.slots.Startingpoint.value);
    //console.log("Ending Value "+intent.slots.Endingpoint.value);
    var MongoClient = require('mongodb').MongoClient;
    var slot = intent.slots.Startingpoint.value;
    var splitted = slot.split(" to ");
    var startingpoint = splitted[0].toUpperCase();
    var endingpoint = splitted[1].toUpperCase();
    startingpoint = ('"' + startingpoint + '"');
    endingpoint = ('"' + endingpoint + '"');
    var starting_busstop = null;
    var ending_busstop = null;
    //console.log(intent.slots.Startingpoint.value);
    MongoClient.connect("mongodb://127.0.0.1:27017", function (err,db) {
        var dbo = db.db("Dynamic_Bus_Scheduling");
        // console.log("starrrrt"+startingpoint);
        const cols = db.db("Dynamic_Bus_Scheduling").collection('BusStopDocuments');
        cols.find({"name":"100 OAKS MALL"}).toArray(function(err, items) {
            starting_busstop=items[0];
            //console.log(items[0]);
            cols.find({"name":"7TH AVE & UNION ST SB"}).toArray(function(err, items) {
                ending_busstop=items[0];
                dbo.collection('TravelRequestDocuments', function (err, collection) {
                    //console.log("starting_busstop"+starting_busstop);
                    collection.insert({
                        "travel_request_document": [{
                            'bus_line_id': "100 Oaks",
                            'starting_bus_stop': starting_busstop,
                            'ending_bus_stop': ending_busstop,
                            'departure_datetime': formatted,
                            'arrival_datetime': "None",
                            'starting_timetable_entry_index': "None",
                            'ending_timetable_entry_index': "None"
                        }]
                    });
            });
        });
        });
    });
    return handlerInput.responseBuilder
        .speak(speechText)
        .getResponse();
}
//app.use(bodyParser.json());
router.post("/", function(req, res){
    if(!skill){
        skill = Alexa.SkillBuilders.custom()
            .addRequestHandlers(
                LaunchRequestHandler,
                BusToIntentHandler
            )
            .create();
    }

    skill.invoke(req.body)
        .then(function(responseBody) {
            res.json(responseBody);
        })
        .catch(function(error) {
            console.log(error);
            res.status(500).send('Error during the request');
        });

});

// app.listen(3000, function () {
//     console.log('Development endpoint listening on port 3000!');
// });
*/


//Algorithm Logic starts here

var BusStop, timetablecollectiondata;

MongoClient.connect(url, function(err, client) {

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
        console.log("number of req");
        console.log(totalNumberOfRequests);
        var totalWaitingTime = 0;

        var totalWaitingTime1 = 0;

        var BusStopArrayEval = [];
        var RequestedArrivingTimeArrayEval = [];

        for(i in items[0]["travel_request_document"]){

            var RequestedArrivingTime = items[0]["travel_request_document"][i].departure_datetime;
            BusStop = (items[0]["travel_request_document"][i].starting_bus_stop.stopid)

            BusStopArrayEval.push(BusStop);
            RequestedArrivingTimeArrayEval.push(RequestedArrivingTime);

            // console.log("bus stop is:")
            // console.log(BusStop);
            var ArrivingTimes = GetArrivingTimes(BusStop)
            //console.log(items[0]["travel_request_document"][i].departure_datetime)
           // console.log("minimum time of minimum")
            //console.log(ArrivingTimes)
            var minimumTime = GetMinimumWaitingTimeForTravelRequest(RequestedArrivingTime, ArrivingTimes)
            //console.log(minimumTime)
            if (typeof minimumTime != 'undefined')
            totalWaitingTime = totalWaitingTime+minimumTime;

        }
        client.close();
        console.log("total waiting time is")
        console.log(totalWaitingTime)
        var AverageWaitingTime = totalWaitingTime/totalNumberOfRequests;
        console.log(AverageWaitingTime);


        if(AverageWaitingTime >= 900) {
            console.log("scheduling a bus");

            var currTime = new Date();
            console.log(currTime);
            console.log(currTime.getHours());
            console.log(currTime.getMinutes());

            var newHour = currTime.getHours();
            var NewTimes = dynamicBusData(newHour,"30");
            //calculate new waiting times.
            var newTimeFromMethod = CalculateNewWaitingTime(NewTimes,BusStopArrayEval,RequestedArrivingTimeArrayEval);
            console.log("old average wait time")
            console.log(AverageWaitingTime/60)
            console.log("new average wait time")
            console.log((newTimeFromMethod/totalNumberOfRequests)/60)
        }
        else {
            console.log("Bus is not Scheduled")
            //dynamicBusData("9","30");
        }
    })
});

function GetArrivingTimes(busStop) {
    for(i in timetablecollectiondata[0]["timetable"]) {
        //console.log("printing next");

        //console.log(i)
        //    console.log(items[0][i])
        //console.log(items[0]["timetable"][i].busstop);
        //console.log(timetablebus)

        if(timetablecollectiondata[0]["timetable"][i].busstop == busStop)
        {
            // console.log("timetable ka busstop");
            // console.log(timetablecollectiondata[0]["timetable"][i].busstop)
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
        if(RequestedArrivingTimeInSeconds<=ArrivingTimesInSeconds)
        WaitingTimes.push(Math.abs(ArrivingTimesInSeconds-RequestedArrivingTimeInSeconds));
    }
    var MinimumWaitingTime = FindMinimumWaitingTimes(WaitingTimes);
            // console.log("requested arriving times is:");
            // console.log(RequestedArrivingTime);
            // console.log("all ariving times are:");
            // console.log(ArrivingTimes);
            // console.log("minimum time is:");
            // console.log(MinimumWaitingTime/60);
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

function CalculateNewWaitingTime(NewTimes,BusStopArrayEval,RequestedArrivingTimeArrayEval)
{
    // console.log("inside calculateNewWaitingTime")
    // console.log("newTimes is:")
    // console.log(NewTimes)
    // console.log("BusStopArrayEval is:")
    // console.log(BusStopArrayEval)
    console.log("RequestedArrivingTimeArrayEval is:")
    console.log(RequestedArrivingTimeArrayEval)

    var NewArrivingTimes = NewTimes[0].NewArrivingTimes;
    var routes = NewTimes[0].route;
    var NewWaitingTime = 0;
    for(var i in RequestedArrivingTimeArrayEval)
    {
        console.log("printing i");
        console.log(i);
        var indexOfNewArrivingTimes = routes.indexOf(BusStopArrayEval[i]);
        NewWaitingTime = NewWaitingTime + Math.abs(GetSecondsFromTime(NewArrivingTimes[indexOfNewArrivingTimes])-GetSecondsFromTime(RequestedArrivingTimeArrayEval[i]));
    }
    return NewWaitingTime;
}

function dynamicBusData(NewStartHour, NewStartMinute)
{
     var NewStartHour = "15";
    var NewStartMinute = "15"
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

    //returning template document
    return template;
}

module.exports = router;
