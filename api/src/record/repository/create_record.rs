use sqlx;

use super::Repository;
use crate::{db::Queryer, errors::app::Error, record::entities};

impl Repository {
    pub async fn create_record<'c, C: Queryer<'c>>(
        &self,
        db: C,
        record: &entities::CreateRecord,
    ) -> Result<entities::RecordEntity, Error> {
        const QUERY: &str = "insert into record (owner, zone_id, rtype_id, ttl_id) values ($1, $2, $3, $4) returning *";

        match sqlx::query_as::<_, entities::RecordEntity>(QUERY)
            .bind(&record.owner)
            .bind(record.zone_id)
            .bind(record.rtype_id)
            .bind(record.ttl_id)
            .fetch_one(db)
            .await
        {
            Err(err) => {
                tracing::error!("{}", &err);
                Err(err.into())
            }
            Ok(record) => Ok(record),
        }
    }
}
