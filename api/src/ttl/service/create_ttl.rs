use super::{CreateTtlInput, Service};
use crate::{errors::app::Error, ttl::entities};

impl Service {
    pub async fn create_ttl(&self, input: CreateTtlInput) -> Result<entities::Ttl, crate::Error> {
        // guard
        let ttl_exists = self.check_ttl_exists(&self.db, input.time).await?;
        if ttl_exists {
            return Err(Error::TtlAlreadyExists.into());
        }

        let ttl_input = entities::CreateTtl { time: input.time };
        let ttl = self.repo.create_ttl(&self.db, &ttl_input).await?;
        entities::Ttl::try_from(ttl)
    }
}
