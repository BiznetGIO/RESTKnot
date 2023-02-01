mod create_record;
mod find_record;
mod find_records;

use std::sync::Arc;

use crate::{db::DB, record::repository::Repository, rtype, scalar::Id, ttl};

#[derive(Debug)]
pub struct Service {
    repo: Repository,
    pub db: DB,
    rtype_service: Arc<rtype::Service>,
    ttl_service: Arc<ttl::Service>,
}

impl Service {
    pub fn new(db: DB, rtype_service: Arc<rtype::Service>, ttl_service: Arc<ttl::Service>) -> Self {
        let repo = Repository::new();
        Self {
            db,
            repo,
            rtype_service,
            ttl_service,
        }
    }
}

#[derive(Debug)]
pub struct CreateRecordInput {
    pub zone: String,
    pub owner: String,
    pub rtype: String,
    pub rdata: String,
    pub ttl: i32,
}

#[derive(Debug)]
pub struct UpdateRecordInput {
    pub id: Id,
    pub zone: String,
    pub owner: String,
    pub rtype: String,
    pub rdata: String,
    pub ttl: i32,
}
