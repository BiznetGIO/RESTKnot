mod check_ttl_exists;
mod create_ttl;
mod delete_ttl;
mod find_ttl;
mod find_ttl_by_time;
mod find_ttls;
mod update_ttl;

use crate::{db::DB, scalar::Id, ttl::repository::Repository};

#[derive(Debug)]
pub struct Service {
    repo: Repository,
    pub db: DB,
}

impl Service {
    pub fn new(db: DB) -> Self {
        let repo = Repository::new();
        Self { db, repo }
    }
}

#[derive(Debug)]
pub struct CreateTtlInput {
    pub time: i32,
}

#[derive(Debug)]
pub struct UpdateTtlInput {
    pub id: Id,
    pub time: i32,
}
