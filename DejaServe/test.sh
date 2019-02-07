curl -X GET http://localhost:8080/process
curl -X POST -d data=google --max-time 10 http://localhost:8080/process
curl -X DELETE -d data=google --max-time 10 http://localhost:8080/process
curl -X PUT -d data=google --max-time 10 http://localhost:8080/process
curl -X GET --max-time 10 http://localhost:8080/stats
