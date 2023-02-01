use super::Service;
use crate::record::entities;

impl Service {
    pub async fn find_records(&self) -> Result<Vec<entities::Record>, crate::Error> {
        let records = self.repo.find_all_records(&self.db).await?;
        let records: Result<Vec<entities::Record>, _> = records
            .into_iter()
            .map(entities::Record::try_from)
            .collect();

        match records.ok() {
            None => Err(crate::Error::InvalidArgument(
                "failed to convert record".into(),
            )),
            Some(records) => Ok(records),
        }
    }
}
