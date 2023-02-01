use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct HealthResponse {
    pub data: Health,
}

#[derive(Debug, Deserialize)]
pub struct Health {
    pub status: String,
}
