use super::{CreateRecordInput, Service};
use crate::record::entities;

impl Service {
    pub async fn create_record(
        &self,
        input: CreateRecordInput,
    ) -> Result<entities::Record, crate::Error> {
        // let recordname_exists = self.check_record_exists(&self.db, &input.email).await?;
        // if recordname_exists {
        //     return Err(Error::RecordAlreadyExists.into());
        // }

        let zone = self.repo.find_zone_by_name(&self.db, input.zone).await?;
        let rtype = self.rtype_service.find_rtype_by_type(&input.rtype).await?;
        let ttl = self.ttl_service.find_ttl_by_time(input.ttl).await?;

        let record_input = entities::CreateRecord {
            owner: input.owner,
            zone_id: zone.id,
            rtype_id: rtype.id,
            ttl_id: ttl.id,
        };

        let record = self.repo.create_record(&self.db, &record_input).await?;
        let record = self.find_record(record.id).await?;
        Ok(record)
    }
}
