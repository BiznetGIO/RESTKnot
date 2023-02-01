use sqlx;

use crate::scalar::Id;

#[derive(sqlx::FromRow, Debug, Clone)]
pub struct Rtype {
    pub id: Id,
    pub rtype: String,
}

#[derive(sqlx::FromRow, Debug, Clone)]
pub struct CreateRtype {
    pub rtype: String,
}
