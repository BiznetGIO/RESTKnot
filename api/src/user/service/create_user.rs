use chrono::Utc;

use super::{CreateUserInput, Service};
use crate::{errors::app::Error, user::entities};

impl Service {
    pub async fn create_user(
        &self,
        input: CreateUserInput,
    ) -> Result<entities::User, crate::Error> {
        // guard
        let username_exists = self.check_user_exists(&self.db, &input.email).await?;
        if username_exists {
            return Err(Error::UsernameAlreadyExists.into());
        }

        let user_input = entities::CreateUser {
            email: input.email,
            created_at: Utc::now().naive_local(),
        };
        let user = self.repo.create_user(&self.db, &user_input).await?;
        Ok(user)
    }
}
