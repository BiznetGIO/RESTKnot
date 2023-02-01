mod create_rtype;
mod delete_rtype;
mod find_all_rtypes;
mod find_rtype_by_id;
mod find_rtype_by_type;
mod update_rtype;

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
