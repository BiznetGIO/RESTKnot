use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, rtype::entities, scalar::Id};

impl Repository {
    pub async fn find_rtype_by_id<'c, C: Queryer<'c>>(
        &self,
        db: C,
        id: Id,
    ) -> Result<entities::Rtype, Error> {
        const QUERY: &str = "select * from type where id = $1";

        match sqlx::query_as::<_, entities::Rtype>(QUERY)
            .bind(id)
            .fetch_optional(db)
            .await
        {
            Err(err) => {
                tracing::error!("{}", &err);
                Err(err.into())
            }
            Ok(None) => Err(Error::RtypeNotFound),
            Ok(Some(res)) => Ok(res),
        }
    }
}
