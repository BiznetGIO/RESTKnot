use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, rtype::entities, scalar::Id};

impl Repository {
    pub async fn delete_rtype<'c, C: Queryer<'c>>(
        &self,
        db: C,
        id: Id,
    ) -> Result<entities::Rtype, Error> {
        const QUERY: &str = "delete from type where id = $1 returning *";

        match sqlx::query_as::<_, entities::Rtype>(QUERY)
            .bind(id)
            .fetch_one(db)
            .await
        {
            Err(err) => {
                tracing::error!("{}", &err);
                Err(err.into())
            }
            Ok(rtype) => Ok(rtype),
        }
    }
}
