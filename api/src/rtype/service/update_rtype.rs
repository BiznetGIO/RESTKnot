use super::{Service, UpdateRtypeInput};
use crate::{errors::app::Error, rtype::entities};

impl Service {
    pub async fn update_rtype(
        &self,
        input: UpdateRtypeInput,
    ) -> Result<entities::Rtype, crate::Error> {
        let rtypename_exists = self.check_rtype_exists(&self.db, &input.rtype).await?;
        if rtypename_exists {
            return Err(Error::RtypeAlreadyExists.into());
        }

        let rtype_input = entities::Rtype {
            id: input.id,
            rtype: input.rtype,
        };

        let rtype = self.repo.update_rtype(&self.db, &rtype_input).await?;

        Ok(rtype)
    }
}
