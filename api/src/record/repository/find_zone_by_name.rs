use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, record::entities};

impl Repository {
    pub async fn find_zone_by_name<'c, C: Queryer<'c>>(
        &self,
        db: C,
        name: String,
    ) -> Result<entities::Zone, Error> {
        const QUERY: &str = "SELECT * FROM zone WHERE name = $1";

        match sqlx::query_as::<_, entities::Zone>(QUERY)
            .bind(name)
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
