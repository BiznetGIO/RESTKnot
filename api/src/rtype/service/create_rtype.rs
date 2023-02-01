use super::{CreateRtypeInput, Service};
use crate::{errors::app::Error, rtype::entities};

impl Service {
    pub async fn create_rtype(
        &self,
        input: CreateRtypeInput,
    ) -> Result<entities::Rtype, crate::Error> {
        let rtype_exists = self.check_rtype_exists(&self.db, &input.rtype).await?;
        if rtype_exists {
            return Err(Error::RtypeAlreadyExists.into());
        }

        let rtype_input = entities::CreateRtype { rtype: input.rtype };

        let rtype = self.repo.create_rtype(&self.db, &rtype_input).await?;

        Ok(rtype)
    }
}
