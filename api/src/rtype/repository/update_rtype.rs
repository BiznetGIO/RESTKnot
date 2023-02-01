use sqlx;

use super::Repository;
use crate::{db, errors::app::Error, rtype::entities};

impl Repository {
    pub async fn update_rtype<'c, C: db::Queryer<'c>>(
        &self,
        db: C,
        rtype: &entities::Rtype,
    ) -> Result<entities::Rtype, Error> {
        const QUERY: &str = "update type set
              type = $2
           where id = $1 returning *";

        match sqlx::query_as::<_, entities::Rtype>(QUERY)
            .bind(rtype.id)
            .bind(&rtype.rtype)
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
