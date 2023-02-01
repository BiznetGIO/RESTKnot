use super::Service;
use crate::{record::entities, scalar::Id};

impl Service {
    pub async fn find_record(&self, id: Id) -> Result<entities::Record, crate::Error> {
        let record = self.repo.find_record_by_id(&self.db, id).await?;
        let rdata = self.repo.find_rdata_by_id(&self.db, record.id).await?;
        let zone = self.repo.find_zone_by_id(&self.db, record.zone_id).await?;
        let rtype = self.rtype_service.find_rtype(record.type_id).await?;
        let ttl = self.ttl_service.find_ttl(record.ttl_id).await?;

        let record = entities::Record {
            id: record.id,
            zone,
            owner: record.owner,
            rtype: rtype.rtype,
            rdata: rdata.data,
            ttl: ttl.time,
        };
        Ok(record)
    }
}
