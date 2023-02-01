use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, scalar::Id, ttl::entities};

impl Repository {
    pub async fn delete_ttl<'c, C: Queryer<'c>>(
        &self,
        db: C,
        id: Id,
    ) -> Result<entities::TtlLegacy, Error> {
        const QUERY: &str = "delete from ttl where id = $1 returning *";

        match sqlx::query_as::<_, entities::TtlLegacy>(QUERY)
            .bind(id)
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
