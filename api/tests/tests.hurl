# REST API health
# hurl --test tests/tests.hurl

GET http://127.0.0.1:5000/health

HTTP/1.1 200
[Asserts]
status == 200
jsonpath "$.data.status" == "running"

# meta
GET http://127.0.0.1:5000/meta

HTTP/1.1 200
[Asserts]
status == 200
jsonpath "$.data.build" == "unknown"
