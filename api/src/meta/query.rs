use axum::{Extension, Json};
use std::sync::Arc;

use crate::context::ServerContext;
use crate::meta::model;

// utoipa can't find `model::<StructName>`
#[allow(unused_imports)]
use crate::meta::model::{Config, Version};

#[utoipa::path(
    get,
    path = "/meta/version",
    responses(
        (status = 200, description = "Get meta information", body = MetaResponse),
    ),
)]
pub async fn version(
    ctx: Extension<Arc<ServerContext>>,
) -> Result<Json<model::VersionResponse>, crate::Error> {
    let meta = ctx.meta_service.get_version().await?;

    let response = model::VersionResponse { data: meta.into() };
    Ok(Json(response))
}

#[utoipa::path(
    get,
    path = "/meta/config",
    responses(
        (status = 200, description = "Get config information", body = ConfigResponse),
    ),
)]
pub async fn config(
    ctx: Extension<Arc<ServerContext>>,
) -> Result<Json<model::ConfigResponse>, crate::Error> {
    let meta = ctx.meta_service.get_config().await?;

    let response = model::ConfigResponse { data: meta.into() };
    Ok(Json(response))
}
