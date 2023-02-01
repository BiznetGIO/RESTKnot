use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, user::entities};

impl Repository {
    pub async fn create_user<'c, C: Queryer<'c>>(
        &self,
        db: C,
        user: &entities::CreateUser,
    ) -> Result<entities::User, Error> {
        const QUERY: &str = "insert into \"user\" (email, created_at) values ($1, $2) returning *";

        match sqlx::query_as::<_, entities::User>(QUERY)
            .bind(&user.email)
            .bind(user.created_at)
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
