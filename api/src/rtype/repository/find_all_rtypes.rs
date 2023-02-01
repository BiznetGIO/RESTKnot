use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, rtype::entities};

impl Repository {
    pub async fn find_all_rtypes<'c, C: Queryer<'c>>(
        &self,
        db: C,
    ) -> Result<Vec<entities::Rtype>, Error> {
        const QUERY: &str = "select * from type ORDER BY id";

        match sqlx::query_as::<_, entities::Rtype>(QUERY)
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
