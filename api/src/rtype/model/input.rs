use axum_typed_multipart::TryFromMultipart;

use crate::scalar::Id;

#[derive(TryFromMultipart)]
pub struct CreateRtypeInput {
    /// The record type
    pub rtype: String,
}

#[derive(TryFromMultipart)]
pub struct UpdateRtypeInput {
    /// The record type
    pub rtype: String,
}

#[derive(TryFromMultipart)]
pub struct DeleteRtypeInput {
    /// The ID of the Trtype to modify.
    pub id: Id,
}
