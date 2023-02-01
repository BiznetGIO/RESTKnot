use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, rtype::entities};

impl Repository {
    pub async fn find_rtype_by_type<'c, C: Queryer<'c>>(
        &self,
        db: C,
        rtype: &str,
    ) -> Result<entities::Rtype, Error> {
        const QUERY: &str = "select * from type where type = $1";

        match sqlx::query_as::<_, entities::Rtype>(QUERY)
            .bind(rtype)
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
