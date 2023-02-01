use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, record::entities, scalar::Id};

impl Repository {
    pub async fn find_zone_by_id<'c, C: Queryer<'c>>(
        &self,
        db: C,
        id: Id,
    ) -> Result<entities::Zone, Error> {
        const QUERY: &str = "SELECT * FROM zone WHERE id = $1";

        match sqlx::query_as::<_, entities::Zone>(QUERY)
            .bind(id)
            .fetch_optional(db)
            .await
        {
            Err(err) => {
                tracing::error!("{}", &err);
                Err(err.into())
            }
            Ok(None) => Err(Error::ZoneNotFound),
            Ok(Some(zone)) => Ok(zone),
        }
    }
}
