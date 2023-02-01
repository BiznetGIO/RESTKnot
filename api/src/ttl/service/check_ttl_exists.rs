use super::Service;
use crate::{db::Queryer, errors::app::Error};

impl Service {
    /// returns true if a ttlname exists. false otherwise
    pub async fn check_ttl_exists<'c, C: Queryer<'c>>(
        &self,
        db: C,
        time: i32,
    ) -> Result<bool, crate::Error> {
        let find_existing_ttl = self.repo.find_ttl_by_time(db, time).await;
        match find_existing_ttl {
            Ok(_) => Ok(true),
            Err(Error::TtlNotFound) => Ok(false),
            Err(err) => Err(err.into()),
        }
    }
}
