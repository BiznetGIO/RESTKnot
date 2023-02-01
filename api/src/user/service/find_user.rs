use super::Service;
use crate::{scalar::Id, user::entities};

impl Service {
    pub async fn find_user(&self, id: Id) -> Result<entities::User, crate::Error> {
        let user = self.repo.find_user_by_id(&self.db, id).await?;

        Ok(user)
    }
}
