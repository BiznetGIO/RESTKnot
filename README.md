[![Build Status](https://travis-ci.org/riszkymf/RESTKnot.svg?branch=testcase_travis)](https://travis-ci.org/riszkymf/RESTKnot)

# REST KNOT
Restknot is a Knot based DNS management system that simplify DNS configuration on Knot Server. Consists of three applications : Agent, API, and CLI. API manages DNS which then will be configured to knot server by Agent. Both of this apps is accessible from CLI.


## Features



----------------------
## API
### Requirements :
- [redis](API/README.md)
- [CockroachDB](https://www.cockroachlabs.com/docs/stable/install-cockroachdb-linux.html)




Further information on API read [API Documentation](API/README.md)


## AGENT
### Requirements : 
- [Knot-DNS](https://www.knot-dns.cz/download/)

Further information on API read [AGENT Documentation](AGENT/README.md)


## CLI

[Documentation](CLI/README.md)
