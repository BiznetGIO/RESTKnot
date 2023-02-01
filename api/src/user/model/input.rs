use axum_typed_multipart::TryFromMultipart;

use crate::scalar::Id;

#[derive(TryFromMultipart)]
pub struct CreateUserInput {
    /// The email for the User.
    pub email: String,
}

#[derive(TryFromMultipart)]
pub struct UpdateUserInput {
    /// The email for the User.
    pub email: String,
}

#[derive(TryFromMultipart)]
pub struct DeleteUserInput {
    /// The ID of the User to modify.
    pub id: Id,
}
