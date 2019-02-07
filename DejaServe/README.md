#Python version:
3.6.7

# Run Test Script to Test Quickly as :-
bash test.sh

#POST Request:-

curl -X POST -d data=google http://localhost:8080/process

#PUT Request:-

curl -X PUT -d data=google http://localhost:8080/process

#Delete Request:-

curl -X DELETE -d data=google http://localhost:8080/proces

#GET Request:-

curl -X GET http://localhost:8080/process

#Stats Request:-

curl -X GET http://localhost:8080/stats


