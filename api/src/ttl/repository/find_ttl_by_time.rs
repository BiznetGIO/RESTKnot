use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, ttl::entities};

impl Repository {
    pub async fn find_ttl_by_time<'c, C: Queryer<'c>>(
        &self,
        db: C,
        time: i32,
    ) -> Result<entities::TtlLegacy, Error> {
        const QUERY: &str = "select * from ttl where ttl = $1";

        match sqlx::query_as::<_, entities::TtlLegacy>(QUERY)
            .bind(time)
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
