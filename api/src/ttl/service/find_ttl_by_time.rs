use super::Service;
use crate::ttl::entities;

impl Service {
    pub async fn find_ttl_by_time(&self, time: i32) -> Result<entities::Ttl, crate::Error> {
        let ttl = self.repo.find_ttl_by_time(&self.db, time).await?;
        entities::Ttl::try_from(ttl)
    }
}
