use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct VersionResponse {
    pub data: Version,
}

#[derive(Debug, Deserialize)]
pub struct Version {
    pub build: String,
    pub version: String,
}
