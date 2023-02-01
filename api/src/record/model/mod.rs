pub mod input;

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

use crate::{record::entities, scalar::Id};

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct Record {
    /// The ID of the record.
    pub id: Id,
    /// The zone name
    pub zone: Zone,
    /// The record owner
    pub owner: String,
    /// The record type
    pub rtype: String,
    /// The record data
    pub rdata: String,
    /// The time to live
    pub ttl: i32,
}

impl From<entities::Record> for Record {
    fn from(record: entities::Record) -> Self {
        Self {
            id: record.id,
            zone: record.zone.into(),
            owner: record.owner,
            rtype: record.rtype,
            rdata: record.rdata,
            ttl: record.ttl,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct Zone {
    pub id: Id,
    pub name: String,
    pub is_committed: bool,
    pub user_id: Id,
}

impl From<entities::Zone> for Zone {
    fn from(zone: entities::Zone) -> Self {
        Self {
            id: zone.id,
            name: zone.name,
            is_committed: zone.is_committed,
            user_id: zone.user_id,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct Rdata {
    pub id: Id,
    pub rdata: String,
    pub record_id: Id,
}

impl From<entities::Rdata> for Rdata {
    fn from(rdata: entities::Rdata) -> Self {
        Self {
            id: rdata.id,
            rdata: rdata.data,
            record_id: rdata.record_id,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct RecordResponse {
    pub data: Record,
}

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct RecordsResponse {
    pub data: Vec<Record>,
}
