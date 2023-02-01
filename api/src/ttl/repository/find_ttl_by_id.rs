use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, scalar::Id, ttl::entities};

impl Repository {
    pub async fn find_ttl_by_id<'c, C: Queryer<'c>>(
        &self,
        db: C,
        id: Id,
    ) -> Result<entities::TtlLegacy, Error> {
        const QUERY: &str = "select * from ttl where id = $1";

        match sqlx::query_as::<_, entities::TtlLegacy>(QUERY)
            .bind(id)
            .fetch_optional(db)
            .await
        {
            Err(err) => {
                tracing::error!("{}", &err);
                Err(err.into())
            }
            Ok(None) => Err(Error::TtlNotFound),
            Ok(Some(res)) => Ok(res),
        }
    }
}
