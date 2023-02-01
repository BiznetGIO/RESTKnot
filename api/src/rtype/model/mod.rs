pub mod input;

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

use crate::rtype::entities;
use crate::scalar::Id;

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct Rtype {
    /// The ID of the rtype.
    pub id: Id,
    /// The time for the rtype.
    pub rtype: String,
}

impl From<entities::Rtype> for Rtype {
    fn from(t: entities::Rtype) -> Self {
        Self {
            id: t.id,
            rtype: t.rtype,
        }
    }
}

#[derive(Debug, Serialize, ToSchema)]
pub struct RtypeResponse {
    pub data: Rtype,
}

#[derive(Debug, Serialize, ToSchema)]
pub struct RtypesResponse {
    pub data: Vec<Rtype>,
}
