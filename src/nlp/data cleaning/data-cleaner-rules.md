**lat** = `Y`
**lon** = `X`

**time** = a unix timestamp based on `Date` value and `Time` value
**privacy** = "public"
**reportingUser** = "system"
**anonymous** = false
**message** = `description`

**category**
Assign category based on the current category and description:

* NON-CRIMINAL - *delete the record*
* VANDALISM - *delete the record*
* WARRANTS - *delete the record*
* SUSPICIOUS OCC - *delete the record*
* FORGERY/COUNTERFEITING - *delete the record*
* EMBEZZLEMENT - *delete the record*
* FAMILY OFFENSES - *delete the record*
* BAD CHECKS - *delete the record*
* TREA - *delete the record*
* GAMBLING - *delete the record*
* TRESPASS - *delete the record*
* FRAUD - *delete the record*
* RUNAWAY - *delete the record*
* BRIBERY - *delete the record*
* PROSTITUTION - *delete the record*
* PORNOGRAPHY/OBSCENE MAT - *delete the record*
* EXTORTION - *delete the record*

* ROBBERY - Larceny/Theft
* BURGLARY - Larceny/Theft
* LARCENY/THEFT - Larceny/Theft
* VEHICLE THEFT - Larceny/Theft
* RECOVERED VEHICLE - Larceny/Theft
* STOLEN PROPERTY - Larceny/Theft

* ASSAULT - Violence/Homicide
* SECONDARY CODES - Violence/Homicide
* WEAPON LAWS - Violence/Homicide
* ARSON - Violence/Homicide
* DISORDERLY CONDUCT - Violence/Homicide

* DRUG/NARCOTIC - Drug/Narcotics
* DRUNKENNESS - Drug/Narcotics
* LIQUOR LAWS - Drug/Narcotics

* MISSING PERSON - Kidnapping
* KIDNAPPING - Kidnapping

* DRIVING UNDER THE INFLUENCE - Traffic Violation

* SEX OFFENSES, FORCIBLE - Sex Offences
* SEX OFFENSES, NON FORCIBLE - Sex Offences

* SUICIDE - Mental Health/Bullying
* LOITERING - Mental Health/Bullying

* OTHER OFFENSES - depending on the description
  * DRIVERS LICENSE, SUSPENDED OR REVOKED - Traffic Violation
  * FALSE EVIDENCE OF VEHICLE REGISTRATION - Traffic Violation
  * LOST/STOLEN LICENSE PLATE - Traffic Violation
  * RECKLESS DRIVING - Traffic Violation
  * TRAFFIC COLLISION, HIT & RUN, PROPERTY DAMAGE - Traffic Violation
  * TRAFFIC VIOLATION - Traffic Violation
  * TRAFFIC VIOLATION ARREST - Traffic Violation
  * FAILURE TO REGISTER AS SEX OFFENDER - Sex Offences
  * HARASSING PHONE CALLS - Mental Health/Bullying
  * OBSCENE PHONE CALLS(S) - Mental Health/Bullying
  * POSSESSION OF BURGLARY TOOLS - Larceny/Theft
  * POSSESSION OF BURGLARY TOOLS W/PRIORS - Larceny/Theft
  * TAMPERING WITH A VEHICLE - Larceny/Theft
  * Any other - *delete the record*

* Any other - *delete the record*

**status**
Assign status based on the `resolution` field:
* ARREST, BOOKED - solved by police
* ARREST, CITED - solved by police
* CLEARED-CONTACT JUVENILE FOR MORE INFO - solved by police
* EXCEPTIONAL CLEARANCE - solved by police
* JUVENILE BOOKED - solved by police
* NONE - pending
* UNFOUNDED - solved by public
* Any other - *delete the record*