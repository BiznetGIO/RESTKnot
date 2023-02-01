mod create_ttl;
mod delete_ttl;
mod find_all_ttls;
mod find_ttl_by_id;
mod find_ttl_by_time;
mod update_ttl;

#[derive(Debug, Clone)]
pub struct Repository {}

impl Repository {
    pub fn new() -> Repository {
        Repository {}
    }
}

impl Default for Repository {
    fn default() -> Self {
        Self::new()
    }
}
