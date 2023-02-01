use super::Service;
use crate::{scalar::Id, ttl::entities};

impl Service {
    pub async fn find_ttl(&self, id: Id) -> Result<entities::Ttl, crate::Error> {
        let ttl = self.repo.find_ttl_by_id(&self.db, id).await?;
        entities::Ttl::try_from(ttl)
    }
}
