use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

use crate::meta::entities;

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct Version {
    pub build: String,
    pub version: String,
}

impl From<entities::Version> for Version {
    fn from(meta: entities::Version) -> Self {
        Self {
            build: meta.build,
            version: meta.version,
        }
    }
}

#[derive(Debug, Serialize, ToSchema)]
pub struct VersionResponse {
    pub data: Version,
}

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct Config {
    pub brokers: Vec<String>,
    pub servers: Servers,
}

impl From<entities::Config> for Config {
    fn from(c: entities::Config) -> Self {
        Self {
            brokers: c.brokers,
            servers: c.servers.into(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct Servers {
    pub master: Master,
    pub slave: Slave,
}

impl From<entities::Servers> for Servers {
    fn from(s: entities::Servers) -> Self {
        Self {
            master: s.master.into(),
            slave: s.slave.into(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct Master {
    pub notify: Vec<String>,
    pub acl: Vec<String>,
}

impl From<entities::Master> for Master {
    fn from(m: entities::Master) -> Self {
        Self {
            acl: m.acl,
            notify: m.notify,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct Slave {
    pub master: Vec<String>,
    pub acl: Vec<String>,
}

impl From<entities::Slave> for Slave {
    fn from(s: entities::Slave) -> Self {
        Self {
            master: s.master,
            acl: s.acl,
        }
    }
}

#[derive(Debug, Serialize, ToSchema)]
pub struct ConfigResponse {
    pub data: Config,
}
