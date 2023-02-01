use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, scalar::Id, user::entities};

impl Repository {
    pub async fn delete_user<'c, C: Queryer<'c>>(
        &self,
        db: C,
        id: Id,
    ) -> Result<entities::User, Error> {
        const QUERY: &str = "delete from \"user\" where id = $1 returning *";

        match sqlx::query_as::<_, entities::User>(QUERY)
            .bind(id)
            .fetch_one(db)
            .await
        {
            Err(err) => {
                tracing::error!("{}", &err);
                Err(err.into())
            }
            Ok(user) => Ok(user),
        }
    }
}
