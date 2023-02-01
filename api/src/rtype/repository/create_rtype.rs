use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, rtype::entities};

impl Repository {
    pub async fn create_rtype<'c, C: Queryer<'c>>(
        &self,
        db: C,
        rtype: &entities::CreateRtype,
    ) -> Result<entities::Rtype, Error> {
        const QUERY: &str = "insert into type (type) values ($1) returning *";

        match sqlx::query_as::<_, entities::Rtype>(QUERY)
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
