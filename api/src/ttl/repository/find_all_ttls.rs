use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, ttl::entities};

impl Repository {
    pub async fn find_all_ttls<'c, C: Queryer<'c>>(
        &self,
        db: C,
    ) -> Result<Vec<entities::TtlLegacy>, Error> {
        const QUERY: &str = "select * from ttl ORDER BY id";

        match sqlx::query_as::<_, entities::TtlLegacy>(QUERY)
            .fetch_all(db)
            .await
        {
            Err(err) => {
                tracing::error!("{}", &err);
                Err(err.into())
            }
            Ok(res) => Ok(res),
        }
    }
}
