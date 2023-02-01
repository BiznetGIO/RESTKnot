mod check_username_exists;
mod create_user;
mod delete_user;
mod find_user;
mod find_users;
mod update_user;

use crate::{db::DB, scalar::Id, user::repository::Repository};

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
pub struct CreateUserInput {
    pub email: String,
}

#[derive(Debug)]
pub struct UpdateUserInput {
    pub id: Id,
    pub email: String,
}
