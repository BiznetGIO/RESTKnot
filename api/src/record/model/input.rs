use axum_typed_multipart::TryFromMultipart;

use crate::scalar::Id;

#[derive(TryFromMultipart)]
pub struct CreateRecordInput {
    /// The zone name
    pub zone: String,
    /// The record owner
    pub owner: String,
    /// The record type
    pub rtype: String,
    /// The record data
    pub rdata: String,
    /// The time to live
    pub ttl: i32,
}

#[derive(TryFromMultipart)]
pub struct UpdateRecordInput {
    /// The zone name
    pub zone: String,
    /// The record owner
    pub owner: String,
    /// The record type
    pub rtype: String,
    /// The record data
    pub rdata: String,
    /// The time to live
    pub ttl: i32,
}

#[derive(TryFromMultipart)]
pub struct DeleteRecordInput {
    /// The ID of the record to modify.
    pub id: Id,
}
