mod create_record;
mod find_all_records;
mod find_rdata_by_id;
mod find_record_by_id;
mod find_zone_by_id;
mod find_zone_by_name;

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
