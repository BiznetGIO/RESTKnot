use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, user::entities};

impl Repository {
    pub async fn find_user_by_email<'c, C: Queryer<'c>>(
        &self,
        db: C,
        email: &str,
    ) -> Result<entities::User, Error> {
        const QUERY: &str = "select * from \"user\" where email = $1";

        match sqlx::query_as::<_, entities::User>(QUERY)
            .bind(email)
            .fetch_optional(db)
            .await
        {
            Err(err) => {
                tracing::error!("{}", &err);
                Err(err.into())
            }
            Ok(None) => Err(Error::UserNotFound),
            Ok(Some(res)) => Ok(res),
        }
    }
}
