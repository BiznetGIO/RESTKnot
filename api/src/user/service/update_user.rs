use super::{Service, UpdateUserInput};
use crate::{errors::app::Error, user::entities};

impl Service {
    pub async fn update_user(
        &self,
        input: UpdateUserInput,
    ) -> Result<entities::User, crate::Error> {
        // guards
        self.find_user(input.id).await?;

        let username_exists = self.check_user_exists(&self.db, &input.email).await?;
        if username_exists {
            return Err(Error::UsernameAlreadyExists.into());
        }

        let user_input = entities::UpdateUser {
            id: input.id,
            email: input.email,
        };
        let user = self.repo.update_user(&self.db, &user_input).await?;
        Ok(user)
    }
}
