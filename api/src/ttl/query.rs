use std::sync::Arc;

use axum::response::IntoResponse;
use axum::{extract::Path, http::StatusCode, response::Response, Extension, Json};
use axum_typed_multipart::TypedMultipart;

use super::model::input;
use super::{model, service};
use crate::context::ServerContext;

// utoipa can't find `model::<StructName>`
#[allow(unused_imports)]
use crate::ttl::model::Ttl;

#[utoipa::path(
    get,
    path = "/ttl/list",
    responses(
        (status = 200, description = "List all ttls", body = TtlsResponse),
    ),
)]
pub async fn list(
    ctx: Extension<Arc<ServerContext>>,
) -> Result<Json<model::TtlsResponse>, crate::Error> {
    let ttls = ctx.ttl_service.find_ttls().await?;

    let ttls = ttls.into_iter().map(|t| t.into()).collect();
    let response = model::TtlsResponse { data: ttls };
    Ok(Json(response))
}

#[utoipa::path(
    get,
    path = "/ttl/list/:id",
    responses(
        (status = 200, description = "Get a ttl by id", body = TtlResponse),
    ),
)]
pub async fn get(
    ctx: Extension<Arc<ServerContext>>,
    Path(id): Path<i64>,
) -> Result<Json<model::TtlResponse>, crate::Error> {
    let ttl = ctx.ttl_service.find_ttl(id).await?;

    let response = model::TtlResponse { data: ttl.into() };
    Ok(Json(response))
}

#[utoipa::path(
    post,
    path = "/ttl/add",
    responses(
        (status = 201, description = "Create new ttl", body = TtlResponse),
    ),
)]
pub async fn post(
    ctx: Extension<Arc<ServerContext>>,
    TypedMultipart(input::CreateTtlInput { ttl }): TypedMultipart<input::CreateTtlInput>,
) -> Result<Response, crate::Error> {
    let input = service::CreateTtlInput { time: ttl };
    let ttl = ctx.ttl_service.create_ttl(input).await?;
    let response = model::TtlResponse { data: ttl.into() };
    Ok((StatusCode::CREATED, Json(response)).into_response())
}

#[utoipa::path(
    put,
    path = "/ttl/edit/:id",
    responses(
        (status = 200, description = "Update a ttl", body = TtlResponse),
    ),
)]
pub async fn put(
    ctx: Extension<Arc<ServerContext>>,
    Path(id): Path<i64>,
    TypedMultipart(input::UpdateTtlInput { ttl }): TypedMultipart<input::UpdateTtlInput>,
) -> Result<Json<model::TtlResponse>, crate::Error> {
    let input = service::UpdateTtlInput { id, time: ttl };
    let ttl = ctx.ttl_service.update_ttl(input).await?;
    let response = model::TtlResponse { data: ttl.into() };
    Ok(Json(response))
}

#[utoipa::path(
    delete,
    path = "/ttl/delete/:id",
    responses(
        (status = 204, description = "Delete a ttl", body = TtlResponse),
    ),
)]
pub async fn delete(
    ctx: Extension<Arc<ServerContext>>,
    Path(id): Path<i64>,
) -> Result<StatusCode, crate::Error> {
    ctx.ttl_service.delete_ttl(id).await?;
    Ok(StatusCode::NO_CONTENT)
}
