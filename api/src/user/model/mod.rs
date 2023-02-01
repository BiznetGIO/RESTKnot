pub mod input;

use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

use crate::{
    scalar::{Id, Time},
    user::entities,
};

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct User {
    /// The ID of the User.
    pub id: Id,
    /// The email for the User.
    pub email: String,
    pub created_at: Time,
}

impl From<entities::User> for User {
    fn from(user: entities::User) -> Self {
        Self {
            id: user.id,
            email: user.email,
            created_at: user.created_at,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct UserResponse {
    pub data: User,
}

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct UsersResponse {
    pub data: Vec<User>,
}
