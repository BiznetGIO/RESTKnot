use std::fs;

use super::Service;
use crate::{meta::entities, Error};

impl Service {
    pub async fn get_config(&self) -> Result<entities::Config, crate::Error> {
        let content = fs::read_to_string(&self.config.config_location)
            .map_err(|_| Error::NotFound("Configuration is not found".into()))?;
        let config = toml::from_str(&content)
            .map_err(|_| Error::InvalidArgument("Invalid configuration file".into()))?;
        Ok(config)
    }
}
