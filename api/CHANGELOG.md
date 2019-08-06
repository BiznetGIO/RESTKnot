# Changelog
All notable changes to this project will be documented in this file.

## [0.6.8]
### Added
- Exec config command
- New report error on sendcommmand endpoint
- New feature: 
    - zone-clustering
    - multiple master
    - multiple slave
- New action: 
    - Endpoint : sendcommand
        Action :
            - cluster-master : Clustering master
            - cluster-slave  : Clustering Slave
    - Endpoint : record, ttl, content, content_serial
        Action :
            - edit : edit data
- New Endpoint:
    - unset-master
    - unset-slave
- add validation for record (rfc standard)
- add validation for serial record (rfc standard)
- cors agent fixing
- support sendcommand for MX, SOA, SRV Record to libknot format

## [0.6.10]
- Split task slave by priority
- Model Transaction Isolate
- Optimizing Queue Task in List Command
- Removing api mx-insert-zone

