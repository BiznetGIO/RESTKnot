use super::Service;
use crate::user::entities;

impl Service {
    pub async fn find_users(&self) -> Result<Vec<entities::User>, crate::Error> {
        let users = self.repo.find_all_users(&self.db).await?;
        let users: Result<Vec<entities::User>, _> =
            users.into_iter().map(entities::User::try_from).collect();

        match users.ok() {
            None => Err(crate::Error::InvalidArgument(
                "failed to convert user".into(),
            )),
            Some(users) => Ok(users),
        }
    }
}
