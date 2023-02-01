use super::{Service, UpdateTtlInput};
use crate::{errors::app::Error, ttl::entities};

impl Service {
    pub async fn update_ttl(&self, input: UpdateTtlInput) -> Result<entities::Ttl, crate::Error> {
        // guards
        self.find_ttl(input.id).await?;

        let ttlname_exists = self.check_ttl_exists(&self.db, input.time).await?;
        if ttlname_exists {
            return Err(Error::TtlAlreadyExists.into());
        }

        let ttl_input = entities::Ttl {
            id: input.id,
            time: input.time,
        };
        let ttl = self.repo.update_ttl(&self.db, &ttl_input).await?;
        entities::Ttl::try_from(ttl)
    }
}
