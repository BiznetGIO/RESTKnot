use chrono::NaiveDateTime;
use sqlx;

use crate::scalar::Id;

#[derive(sqlx::FromRow, Debug, Clone)]
pub struct User {
    pub id: Id,
    pub email: String,
    pub created_at: NaiveDateTime,
}

#[derive(sqlx::FromRow, Debug, Clone)]
pub struct CreateUser {
    pub email: String,
    pub created_at: NaiveDateTime,
}

#[derive(sqlx::FromRow, Debug, Clone)]
pub struct UpdateUser {
    pub id: Id,
    pub email: String,
}
