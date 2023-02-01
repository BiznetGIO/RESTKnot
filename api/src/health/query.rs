use axum::{Extension, Json};
use std::sync::Arc;

use crate::context::ServerContext;
use crate::health::model;

// utoipa can't find `model::<StructName>`
#[allow(unused_imports)]
use crate::health::model::HealthResponse;

#[utoipa::path(
    get,
    path = "/health",
    responses(
        (status = 200, description = "Get health information", body = HealthResponse),
    ),
)]
pub async fn health(
    ctx: Extension<Arc<ServerContext>>,
) -> Result<Json<model::HealthResponse>, crate::Error> {
    let health = ctx.health_service.get_health().await?;

    let response = model::HealthResponse {
        data: health.into(),
    };
    Ok(Json(response))
}
