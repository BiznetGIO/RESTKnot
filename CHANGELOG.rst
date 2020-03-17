Unreleased
==========

0.7.0 (2020-03-17)
==================

- Add DNS rules (CNAME, A, AAAA, SOA, NS, MX, TXT)
- Add more RDATA validation
- Add documentation, guide, example, and tutorial regarding new 0.7.0 API
- Store node hostname in a static file instead of database
- Fix HTTP code status return
- Reject zone changes if maximum limit reached in a day
- Automatically delegate command on domain creation and deletion
- Minimize talks to Kafka to improve performance
- Create default SOA, NS, and CNAME record when creating a domain
