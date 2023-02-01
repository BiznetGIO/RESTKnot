mod get_config;
mod get_version;

use std::sync::Arc;

use crate::config::Config;

pub struct Service {
    config: Arc<Config>,
}

impl Service {
    pub fn new(config: Arc<Config>) -> Self {
        Self { config }
    }
}
