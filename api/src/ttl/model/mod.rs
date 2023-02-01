pub mod input;

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

use crate::scalar::Id;
use crate::ttl::entities;

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct Ttl {
    /// The ID of the ttl.
    pub id: Id,
    /// The time for the ttl.
    pub time: i32,
}

impl From<entities::Ttl> for Ttl {
    fn from(t: entities::Ttl) -> Self {
        Self {
            id: t.id,
            time: t.time,
        }
    }
}

#[derive(Debug, Serialize, ToSchema)]
pub struct TtlResponse {
    pub data: Ttl,
}

#[derive(Debug, Serialize, ToSchema)]
pub struct TtlsResponse {
    pub data: Vec<Ttl>,
}
