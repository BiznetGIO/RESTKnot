use sqlx;

use crate::scalar::Id;

#[derive(sqlx::FromRow, Debug, Clone)]
pub struct Ttl {
    pub id: Id,
    pub time: i32,
}

#[derive(sqlx::FromRow, Debug, Clone)]
pub struct CreateTtl {
    pub time: i32,
}

/// A struct for a bridge to legacy database
#[derive(sqlx::FromRow, Debug, Clone)]
pub struct TtlLegacy {
    pub id: Id,
    // we used `ttl` instead of `time` in the legacy database
    pub ttl: String,
}

impl TryFrom<TtlLegacy> for Ttl {
    type Error = crate::Error;

    fn try_from(t: TtlLegacy) -> Result<Ttl, crate::Error> {
        let time: i32 = t.ttl.parse()?;
        Ok(Self { id: t.id, time })
    }
}
