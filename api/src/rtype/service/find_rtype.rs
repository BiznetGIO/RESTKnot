use super::Service;
use crate::{rtype::entities, scalar::Id};

impl Service {
    pub async fn find_rtype(&self, id: Id) -> Result<entities::Rtype, crate::Error> {
        let rtype = self.repo.find_rtype_by_id(&self.db, id).await?;

        Ok(rtype)
    }
}
