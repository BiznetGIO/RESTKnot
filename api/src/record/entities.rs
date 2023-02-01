use sqlx;

use crate::scalar::Id;

#[derive(sqlx::FromRow, Debug, Clone)]
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

#[derive(sqlx::FromRow, Debug, Clone)]
// We have to adopt the legacy design
pub struct RecordEntity {
    pub id: Id,
    pub owner: String,
    pub zone_id: Id,
    // Previous database already use `type` instead of `rtype`
    pub type_id: Id,
    pub ttl_id: Id,
}

#[derive(sqlx::FromRow, Debug, Clone)]
pub struct Zone {
    pub id: Id,
    pub name: String,
    pub is_committed: bool,
    pub user_id: Id,
}

#[derive(sqlx::FromRow, Debug, Clone)]
pub struct Rdata {
    pub id: Id,
    pub data: String,
    pub record_id: Id,
}

#[derive(sqlx::FromRow, Debug, Clone)]
pub struct CreateRecord {
    pub owner: String,
    pub zone_id: Id,
    pub rtype_id: Id,
    pub ttl_id: Id,
}
