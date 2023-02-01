mod check_rtype_exists;
mod create_rtype;
mod delete_rtype;
mod find_rtype;
mod find_rtype_by_type;
mod find_rtypes;
mod update_rtype;

use crate::{db::DB, rtype::repository::Repository, scalar::Id};

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
pub struct CreateRtypeInput {
    pub rtype: String,
}

#[derive(Debug)]
pub struct UpdateRtypeInput {
    pub id: Id,
    pub rtype: String,
}
