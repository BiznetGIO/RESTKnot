use super::Service;
use crate::rtype::entities;

impl Service {
    pub async fn find_rtypes(&self) -> Result<Vec<entities::Rtype>, crate::Error> {
        let rtypes = self.repo.find_all_rtypes(&self.db).await?;
        let rtypes: Result<Vec<entities::Rtype>, _> =
            rtypes.into_iter().map(entities::Rtype::try_from).collect();

        match rtypes.ok() {
            None => Err(crate::Error::InvalidArgument(
                "failed to convert rtype".into(),
            )),
            Some(rtypes) => Ok(rtypes),
        }
    }
}
