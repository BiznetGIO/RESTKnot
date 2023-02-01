use super::Service;
use crate::rtype::entities;

impl Service {
    pub async fn find_rtype_by_type(&self, rtype: &str) -> Result<entities::Rtype, crate::Error> {
        let rtype = self.repo.find_rtype_by_type(&self.db, rtype).await?;

        Ok(rtype)
    }
}
