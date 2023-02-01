use sqlx;

use crate::{relay::Base64Cursor, scalar::Id};

#[derive(sqlx::FromRow, Debug, Clone)]
pub struct Ttl {
    pub id: Id,
    pub time: i32,
}

#[derive(sqlx::FromRow, Debug, Clone)]
pub struct TtlEntity {
    pub id: Id,
    // We used `ttl` instead of `time` in the legacy database
    pub ttl: String,
}

impl TryFrom<TtlEntity> for Ttl {
    type Error = crate::Error;

    fn try_from(t: TtlEntity) -> Result<Ttl, crate::Error> {
        let time: i32 = t.ttl.parse()?;
        Ok(Self { id: t.id, time })
    }
}

#[derive(sqlx::FromRow, Debug, Clone)]
pub struct CreateTtl {
    pub time: String,
}

#[derive(Debug)]
pub struct TtlEdge {
    pub node: Ttl,
    pub cursor: String,
}

impl From<Ttl> for TtlEdge {
    fn from(t: Ttl) -> Self {
        let cursor = Base64Cursor::new(t.id).encode();
        Self { node: t, cursor }
    }
}
