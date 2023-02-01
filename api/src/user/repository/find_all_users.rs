use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, user::entities};

impl Repository {
    pub async fn find_all_users<'c, C: Queryer<'c>>(
        &self,
        db: C,
    ) -> Result<Vec<entities::User>, Error> {
        const QUERY: &str = "select * from \"user\" ORDER BY id";

        match sqlx::query_as::<_, entities::User>(QUERY)
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
