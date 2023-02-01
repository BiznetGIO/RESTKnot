use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, ttl::entities};

impl Repository {
    pub async fn create_ttl<'c, C: Queryer<'c>>(
        &self,
        db: C,
        ttl: &entities::CreateTtl,
    ) -> Result<entities::TtlLegacy, Error> {
        const QUERY: &str = "insert into ttl (ttl) values ($1) returning *";

        match sqlx::query_as::<_, entities::TtlLegacy>(QUERY)
            .bind(ttl.time)
            .fetch_one(db)
            .await
        {
            Err(err) => {
                tracing::error!("{}", &err);
                Err(err.into())
            }
            Ok(ttl) => Ok(ttl),
        }
    }
}
