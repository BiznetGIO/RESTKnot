use super::Service;
use crate::{
    relay,
    relay::validation::{convert_params, validate_params},
    ttl::entities,
};

impl Service {
    pub async fn find_ttls(
        &self,
        first: Option<i32>,
        after: Option<&str>,
        last: Option<i32>,
        before: Option<&str>,
    ) -> Result<Vec<entities::TtlEdge>, crate::Error> {
        validate_params(first, last)?;
        let (after_id, before_id) = convert_params(after, before)?;

        let ttls = self
            .repo
            .find_all_ttls(&self.db, first, after_id, last, before_id)
            .await?;
        let ttls: Result<Vec<entities::Ttl>, _> =
            ttls.into_iter().map(entities::Ttl::try_from).collect();

        match ttls.ok() {
            None => Err(crate::Error::InvalidArgument(
                "failed to parse the integer value".into(),
            )),
            Some(ttls) => {
                let ttl_edges: Vec<entities::TtlEdge> =
                    ttls.into_iter().map(|ttl| ttl.into()).collect();
                Ok(ttl_edges)
            }
        }
    }
    pub async fn find_page_info(
        &self,
        first: Option<i32>,
        after: Option<&str>,
        last: Option<i32>,
        before: Option<&str>,
    ) -> Result<relay::PageInfo, crate::Error> {
        let (after_id, before_id) = convert_params(after, before)?;

        let ttls = self
            .repo
            .find_all_ttls(&self.db, first, after_id, last, before_id)
            .await?;

        let page_info = self
            .repo
            .find_page_info(&self.db, &ttls, first, after_id, last, before_id)
            .await?;
        Ok(page_info)
    }
}
