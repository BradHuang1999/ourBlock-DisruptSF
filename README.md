# ourBlock: _Bringing Neighborhood Watch Online_

> You see a middle aged man in a red shirt furiously trying to open a bike lock.

> You're not sure if this man owns the bike or if he's commiting a crime.

> More than 5 minutes pass ... do you call the Police?

#### ourBlock is a community safety app built to make crime reporting easy, fast and transparent. 

<img src="https://github.com/charlielin99/ourBlock/blob/master/pitchdeck/app1.png?raw=true" height="350px" width="190px"></img></br>
<sup><em>f1: An interactive heat map showing crimes in the city so civilians can stay safe.</em></sup>

### Tech Stack
- **Tensorflow classifier/spam filter** was trained using a bag-of-words and stemming technique
- Messages posted to the Ethereum network using **Web3 & Solidity**
- GeoLocation is gathered using **Google Maps API**
- Safe paths to navigate around crime calculated using the **A star algorithm**
- Server side logic is hosted on **AWS Lambda**
- The Police Portal is built on a **Flask framework**
- The Civilian Mobile App is built on **React-Native**
- Implemented crime searching using **Elasticsearch**

<img src="https://github.com/charlielin99/ourBlock/blob/master/pitchdeck/hub1.png?raw=true" height="280px"></img></br>
<sup><em>f2: The police hub; automatically dispatches officers to the most urgent locations.</em></sup>

### How It Works
- Reported crimes are geotagged and passed through a deep learning severity classification algorithm
- Live heat maps are populated based on the severity and the frequency per location using triangulation
- Messages are stored in a Blockchain distributed network across user devices to prevent scaling database costs
- Civilians are incentivized to report with ethereum tokens awarded for reports that help solve crime

#### The result is that civilians can avoid / navigate around danger, search for and be notified of crime that may potential involve them, and police can better allocate resources to tackle incidents by urgency at a minimal cost. The community is also transparent and closer than it ever has been with a "I scratch your back if you scratch mine" mentality. All of this is done with the automation provided by machine learning and the distributed blockchain system.
