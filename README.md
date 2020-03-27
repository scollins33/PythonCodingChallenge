# PYTHON CODING CHALLENGE

### What This Is
An application providing a REST API for querying phone numbers parsed from a file.  
The implementation only has a back-end, a browser or Postman must be used to communicate with it.

### Requirements
Python 3.7+  
Tornado 6.0.4+  ```pip install tornado```  

### Overview
```app.py``` is the entry point. It reads in the text file and parses the phone numbers into a global list to act like the DB. It then starts up the Tornado server with one handler and provides the DB list to it.
  
```models/PhoneNumber.py``` is the Class for, you guessed it, phone numbers. This does all of the parsing on init. It also provides one function (```get_formatted_string```) that returns the phone number as a string.  
> Example: +11 (850) 731-2049 ext 327
  
```handlers/Main.py``` is our only Tornado handler. Each query mode (more on that in a bit) could have been broken out to separate handlers but for now it is simple enough to keep in one file/route. It runs through the DB list based on query parameters to return matches.
  
### The Nitty-gritty  
##### Server Info
The server runs on ```locahost:8080```.
  
##### Route
```/api```  
- This is our only route.  
- You will want to attach the ```mode``` and ```value``` query parameters as well.    
- Example: ```http://localhost:8080/api?mode=full&value=```
  
##### Query Parameters
```mode```  
- What part of the phone number you are searching.
- Valid options: 
    > Example Number: +11 (850) 731-2049 ext 327
    - ```full``` returns all numbers
    - ```country```  searches the **exact** country code (11)
    - ```area``` searches the area code (850)
    - ```prefix``` searches the prefix (731)
    - ```line``` searches the line number (2049)
    - ```extended``` acts as a boolean and returns any number with an extension
- Returns Status 405 if you use an invalid option.

```value```  
- The number or numbers to query with.
- The number(s) just need to exist within part you are searching. ```country``` is the exception as it matches exactly.  
- For example ```?mode=area&value=7``` would return numbers with ```607``` and ```770``` as their area code.
- Each mode has a length limit otherwise it returns Status 405.
    - ```full``` 0 (use ```mode=full&value=```)
    - ```country```  2
    - ```area``` 3
    - ```prefix``` 3
    - ```line``` 4
    - ```extended``` 0 (use ```mode=extended&value=```)
      
##### Response Structure
The Response from the server will be a set Status Code as well as a JSON object with ```status``` and ```payload```.  
  
###### Status Codes
- 200 : success
- 400 : missing argument
- 405 : application error (invalid argument, length, etc)
- 501 : POST is not implemented
  
###### JSON Object
- ```status``` : ```True``` (success) or ```False``` (something went wrong)
- ```payload``` : Stringified list of the search results (also strings) or the error produced


### Example Calls (
```GET localhost:8080/api?mode=country&value=1```
```
{
    "status": true, 
    "payload": "[\"1+ (338) 825-9604\", \"1+ (685) 313-9547\"]"
}
```
  
```GET localhost:8080/api?mode=line&value=73111```
```
{
    "status": false,
    "payload": "Value length (5) too large for Mode length (4)"
}
```
  
```GET localhost:8080/api?mode=extended&value=```
```
{
    "status": true,
    "payload": "[\"(980) 955-2397 ext 327\", \"(884) 293-1530 ext 1020\", \"(440) 493-6158 ext 100\", \"(782) 517-7201 ext 101\", \"11+ (223) 446-2467 ext 10\", \"(934) 695-1114 ext 1101\"]"
}