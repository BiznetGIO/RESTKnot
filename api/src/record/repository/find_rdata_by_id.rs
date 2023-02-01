use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, record::entities, scalar::Id};

impl Repository {
    pub async fn find_rdata_by_id<'c, C: Queryer<'c>>(
        &self,
        db: C,
        id: Id,
    ) -> Result<entities::Rdata, Error> {
        const QUERY: &str = "SELECT * FROM rdata WHERE id = $1";

        match sqlx::query_as::<_, entities::Rdata>(QUERY)
            .bind(id)
            .fetch_optional(db)
            .await
        {
            Err(err) => {
                tracing::error!("{}", &err);
                Err(err.into())
            }
            Ok(None) => Err(Error::RdataNotFound),
            Ok(Some(rdata)) => Ok(rdata),
        }
    }
}
