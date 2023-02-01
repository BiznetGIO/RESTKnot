use std::sync::Arc;

use crate::{health, meta, record, rtype, ttl, user};

#[derive(Clone)]
pub struct ServerContext {
    pub health_service: Arc<health::Service>,
    pub meta_service: Arc<meta::Service>,
    pub ttl_service: Arc<ttl::Service>,
    pub rtype_service: Arc<rtype::Service>,
    pub user_service: Arc<user::Service>,
    pub record_service: Arc<record::Service>,
}
