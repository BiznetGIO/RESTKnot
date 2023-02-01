use sqlx;

use super::Repository;
use crate::{db, errors::app::Error, user::entities};

impl Repository {
    pub async fn update_user<'c, C: db::Queryer<'c>>(
        &self,
        db: C,
        user: &entities::UpdateUser,
    ) -> Result<entities::User, Error> {
        const QUERY: &str = "update \"user\" set
              email = $2
           where id = $1 returning *";

        match sqlx::query_as::<_, entities::User>(QUERY)
            .bind(user.id)
            .bind(&user.email)
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
