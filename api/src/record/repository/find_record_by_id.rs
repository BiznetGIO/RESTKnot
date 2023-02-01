use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, record::entities, scalar::Id};

impl Repository {
    pub async fn find_record_by_id<'c, C: Queryer<'c>>(
        &self,
        db: C,
        id: Id,
    ) -> Result<entities::RecordEntity, Error> {
        const QUERY: &str = "SELECT * FROM record WHERE id = $1";

        match sqlx::query_as::<_, entities::RecordEntity>(QUERY)
            .bind(id)
            .fetch_optional(db)
            .await
        {
            Err(err) => {
                tracing::error!("{}", &err);
                Err(err.into())
            }
            Ok(None) => Err(Error::RecordNotFound),
            Ok(Some(record)) => Ok(record),
        }
    }
}
