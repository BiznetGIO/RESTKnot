use super::Service;
use crate::ttl::entities;

impl Service {
    pub async fn find_ttls(&self) -> Result<Vec<entities::Ttl>, crate::Error> {
        let ttls = self.repo.find_all_ttls(&self.db).await?;
        let ttls: Result<Vec<entities::Ttl>, _> =
            ttls.into_iter().map(entities::Ttl::try_from).collect();

        match ttls.ok() {
            None => Err(crate::Error::InvalidArgument(
                "failed to convert ttl".into(),
            )),
            Some(ttls) => Ok(ttls),
        }
    }
}
