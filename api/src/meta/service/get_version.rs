use super::Service;
use crate::meta::entities;

impl Service {
    pub async fn get_version(&self) -> Result<entities::Version, crate::Error> {
        let meta = entities::Version {
            build: option_env!("VCS_REVISION").unwrap_or("unknown").to_string(),
            version: env!("CARGO_PKG_VERSION").to_string(),
        };
        Ok(meta)
    }
}
