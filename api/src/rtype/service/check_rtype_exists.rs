use super::Service;
use crate::{db::Queryer, errors::app::Error};

impl Service {
    /// returns true if a rtypename exists. false otherwise
    pub async fn check_rtype_exists<'c, C: Queryer<'c>>(
        &self,
        db: C,
        rtype: &str,
    ) -> Result<bool, crate::Error> {
        let find_existing_rtype = self.repo.find_rtype_by_type(db, rtype).await;
        match find_existing_rtype {
            Ok(_) => Ok(true),
            Err(Error::RtypeNotFound) => Ok(false),
            Err(err) => Err(err.into()),
        }
    }
}
