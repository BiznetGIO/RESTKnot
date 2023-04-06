use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

use crate::health::entities;

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct Health {
    pub status: String,
}

impl From<entities::Health> for Health {
    fn from(health: entities::Health) -> Self {
        Self {
            status: health.status,
        }
    }
}

#[derive(Debug, Serialize, ToSchema)]
pub struct HealthResponse {
    pub data: Health,
}
