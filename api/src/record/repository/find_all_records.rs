use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, record::entities};

impl Repository {
    pub async fn find_all_records<'c, C: Queryer<'c>>(
        &self,
        db: C,
    ) -> Result<Vec<entities::Record>, Error> {
        const QUERY: &str = "select * from record ORDER BY id";

        match sqlx::query_as::<_, entities::Record>(QUERY)
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
