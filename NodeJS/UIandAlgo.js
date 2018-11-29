var express = require('express');
var app = express();
const assert = require('assert');
var path = require('path');
const MongoClient = require('mongodb').MongoClient;
//app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'views')));
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');
const port = 9999

// Connection URL
const url = 'mongodb://localhost:27017';

// Database Name
const dbName = 'Dynamic_Bus_Scheduling';

/* GET home page. */
app.get('/', function(req, res, next) {
    res.render('index', { title: 'Nashville Metropolitan Transit Authority' });
});

app.get('/timetable', function(req, res, next) {
    MongoClient.connect(url, function(err, client) {

        //Connecting to Timetable document
        var col = client.db(dbName).collection('Timetable');
        col.find().toArray(function(err, items) {
            res.render('timetable', { title: 'Nashville Metropolitan Transit Authority', timetable: items});
        });
        client.close();
    });
});

app.get('/travelrequest', function(req, res, next) {
    MongoClient.connect(url, function(err, client) {

        //Connecting to Timetable document
        var trd = client.db(dbName).collection('TravelRequestDocuments');
        trd.find().toArray(function(err, items) {
            res.render('travelrequest', { title: 'Nashville Metropolitan Transit Authority', travelrequest: items});
        });
        client.close();
    });
});

app.get('/dynamicbusdata', function(req, res, next) {
    MongoClient.connect(url, function(err, client) {

        //Connecting to Timetable document
        var dbd = client.db(dbName).collection('DynamicBusData');
        dbd.find().toArray(function(err, items) {
            res.render('dynamicbusdata', { title: 'Nashville Metropolitan Transit Authority', dynamicbusdata: items});
        });
        client.close();
    });
});

app.listen(port, () => console.log(`Server started and listening on port ${port}!`))


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

module.exports = app;