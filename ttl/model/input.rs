use async_graphql::InputObject;

use crate::scalar::Id;

#[derive(InputObject)]
pub struct CreateTtlInput {
    /// The time for the ttl.
    pub time: i32,
}

#[derive(InputObject)]
pub struct UpdateTtlInput {
    /// The ID of the Tttl to modify.
    pub id: Id,
    /// The time for the ttl.
    pub time: i32,
}

#[derive(InputObject)]
pub struct DeleteTtlInput {
    pub id: Id,
}
