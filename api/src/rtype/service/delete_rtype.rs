use super::Service;

use crate::{rtype::entities, scalar::Id};

impl Service {
    pub async fn delete_rtype(&self, id: Id) -> Result<entities::Rtype, crate::Error> {
        let rtype = self.repo.delete_rtype(&self.db, id).await?;

        Ok(rtype)
    }
}
