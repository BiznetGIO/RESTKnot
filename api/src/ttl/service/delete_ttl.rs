use super::Service;
use crate::{scalar::Id, ttl::entities};

impl Service {
    pub async fn delete_ttl(&self, id: Id) -> Result<entities::Ttl, crate::Error> {
        // guard
        self.find_ttl(id).await?;

        let ttl = self.repo.delete_ttl(&self.db, id).await?;
        entities::Ttl::try_from(ttl)
    }
}
