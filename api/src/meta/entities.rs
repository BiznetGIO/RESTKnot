use serde::Deserialize;

#[derive(Debug)]
pub struct Version {
    pub build: String,
    pub version: String,
}

#[derive(Debug, Deserialize)]
pub struct Config {
    pub brokers: Vec<String>,
    pub servers: Servers,
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Servers {
    pub master: Master,
    pub slave: Slave,
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Master {
    pub notify: Vec<String>,
    pub acl: Vec<String>,
}

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Slave {
    pub master: Vec<String>,
    pub acl: Vec<String>,
}
