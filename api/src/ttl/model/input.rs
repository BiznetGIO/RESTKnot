use axum_typed_multipart::TryFromMultipart;

use crate::scalar::Id;

#[derive(TryFromMultipart)]
pub struct CreateTtlInput {
    /// The time for the ttl.
    pub ttl: i32,
}

#[derive(TryFromMultipart)]
pub struct UpdateTtlInput {
    /// The time for the ttl.
    pub ttl: i32,
}

#[derive(TryFromMultipart)]
pub struct DeleteTtlInput {
    pub id: Id,
}
