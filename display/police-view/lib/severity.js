const weights = {
    police: {
        distance: -0.1 / 1000,
        category: 1,
        time: -10 / (1000 * 1000 * 60 * 60 * 24),
        upovtes: 0.1,
        downvotes: -0.2,
        followers: 0.2,
        status: 1
    },
    civilian: {
        distance: -1,
        category: 1,
        time: 1,
        upovtes: 1,
        downvotes: -1,
        followers: 1, 
        status: 1  
    }
}

const categoryWeights = {
    "Larceny/Theft": 0.3,
    "Violence/Homicide": 1,
    "Mental Health/Bullying": 0.6,
    "Drug/Narcotics": 0.5,
    "Kidnapping": 0.9,
    "Traffic Violation": 0.4,
    "Sex Offences": 0.6
}

const statusWeights = {
    "solved by police": 0.001,
    "solved by public": 0.01,
    "in progress": 0.1,
    "pending": 1
}

function getDistance(currLat, currLon, docLat, docLon) {
	var R = 6371000; // meters (change this constant 6371 to get km, 3963 to get miles)
	var dLat = (docLat - currLat) * Math.PI / 180;
	var dLon = (docLon - currLon) * Math.PI / 180;
	var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
		Math.cos(currLat * Math.PI / 180 ) * Math.cos(docLat * Math.PI / 180 ) *
		Math.sin(dLon/2) * Math.sin(dLon/2);
	var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    var d = R * c;
	return d;
}

function getSeverity (role, currentTime, currLat, currLon, doc) {
    doc.categoryCoef = categoryWeights[doc.category];
    doc.statusCoef = statusWeights[doc.status];
    doc.distance = getDistance(currLat, currLon, doc.lat, doc.lon);

    // console.log("distance", weights[role].distance * doc.distance);
    // console.log("category", weights[role].category * doc.categoryCoef);
    // console.log("time", weights[role].time * (currentTime - doc.time));
    // console.log("upovtes", weights[role].upovtes * doc.upvoterCount);
    // console.log("downvotes", weights[role].downvotes * doc.downvoterCount );
    // console.log("followers", weights[role].followers * doc.followerCount);

    return (
        weights[role].status * doc.statusCoef +
        weights[role].distance * doc.distance +
        weights[role].category * doc.categoryCoef +
        weights[role].time * (currentTime - doc.time) +
        weights[role].upovtes * doc.upvoterCount +
        weights[role].downvotes * doc.downvoterCount +
        weights[role].followers * doc.followerCount
    );
}

function sortBySeverity (role, currentTime, currLat, currLon, docs) {
    docs.forEach(doc => {
        doc.severity = getSeverity(role, currentTime, currLat, currLon, doc);
    });
    return docs.sort((doc1, doc2) => doc2.severity - doc1.severity);
}

function getTopSeverity (role, currentTime, currLat, currLon, docs, topNum) {
    return sortBySeverity(role, currentTime, currLat, currLon , docs).slice(0, topNum);
}

export default {
    getSeverity: getSeverity,
    sortBySeverity: sortBySeverity,
    getTopSeverity: getTopSeverity
}
