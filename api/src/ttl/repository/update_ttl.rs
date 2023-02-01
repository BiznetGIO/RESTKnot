use sqlx;

use super::Repository;
use crate::{db, errors::app::Error, ttl::entities};

impl Repository {
    pub async fn update_ttl<'c, C: db::Queryer<'c>>(
        &self,
        db: C,
        ttl: &entities::Ttl,
    ) -> Result<entities::TtlLegacy, Error> {
        const QUERY: &str = "update ttl set
              ttl = $2
           where id = $1 returning *";

        match sqlx::query_as::<_, entities::TtlLegacy>(QUERY)
            .bind(ttl.id)
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
