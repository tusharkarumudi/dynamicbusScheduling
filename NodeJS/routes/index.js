var express = require('express');
var router = express.Router();
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');
const Alexa = require('ask-sdk-core')

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


module.exports = router;
