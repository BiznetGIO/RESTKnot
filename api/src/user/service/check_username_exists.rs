use super::Service;
use crate::{db::Queryer, errors::app::Error};

impl Service {
    /// returns true if a username exists. false otherwise
    pub async fn check_user_exists<'c, C: Queryer<'c>>(
        &self,
        db: C,
        name: &str,
    ) -> Result<bool, crate::Error> {
        let find_existing_user = self.repo.find_user_by_email(db, name).await;
        match find_existing_user {
            Ok(_) => Ok(true),
            Err(Error::UserNotFound) => Ok(false),
            Err(err) => Err(err.into()),
        }
    }
}
