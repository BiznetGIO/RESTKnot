use super::Service;
use crate::{scalar::Id, user::entities};

impl Service {
    pub async fn delete_user(&self, id: Id) -> Result<entities::User, crate::Error> {
        // guard
        self.find_user(id).await?;

        let user = self.repo.delete_user(&self.db, id).await?;
        Ok(user)
    }
}
