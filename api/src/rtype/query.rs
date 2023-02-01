use std::sync::Arc;

use axum::response::IntoResponse;
use axum::{extract::Path, http::StatusCode, response::Response, Extension, Json};
use axum_typed_multipart::TypedMultipart;

use super::model::input;
use super::{model, service};
use crate::context::ServerContext;

// utoipa can't find `model::<StructName>`
#[allow(unused_imports)]
use crate::rtype::model::Rtype;

#[utoipa::path(
    get,
    path = "/rtype/list",
    responses(
        (status = 200, description = "List all rtypes", body = RtypesResponse),
    ),
)]
pub async fn list(
    ctx: Extension<Arc<ServerContext>>,
) -> Result<Json<model::RtypesResponse>, crate::Error> {
    let rtypes = ctx.rtype_service.find_rtypes().await?;

    let rtypes = rtypes.into_iter().map(|t| t.into()).collect();
    let response = model::RtypesResponse { data: rtypes };
    Ok(Json(response))
}

#[utoipa::path(
    get,
    path = "/rtype/list/:id",
    responses(
        (status = 200, description = "Get a rtype by id", body = RtypeResponse),
    ),
)]
pub async fn get(
    ctx: Extension<Arc<ServerContext>>,
    Path(id): Path<i64>,
) -> Result<Json<model::RtypeResponse>, crate::Error> {
    let rtype = ctx.rtype_service.find_rtype(id).await?;

    let response = model::RtypeResponse { data: rtype.into() };
    Ok(Json(response))
}

#[utoipa::path(
    post,
    path = "/rtype/add",
    responses(
        (status = 201, description = "Create new rtype", body = RtypeResponse),
    ),
)]
pub async fn post(
    ctx: Extension<Arc<ServerContext>>,
    TypedMultipart(input::CreateRtypeInput { rtype }): TypedMultipart<input::CreateRtypeInput>,
) -> Result<Response, crate::Error> {
    let input = service::CreateRtypeInput { rtype };
    let rtype = ctx.rtype_service.create_rtype(input).await?;
    let response = model::RtypeResponse { data: rtype.into() };
    Ok((StatusCode::CREATED, Json(response)).into_response())
}

#[utoipa::path(
    put,
    path = "/rtype/edit/:id",
    responses(
        (status = 200, description = "Update a rtype", body = RtypeResponse),
    ),
)]
pub async fn put(
    ctx: Extension<Arc<ServerContext>>,
    Path(id): Path<i64>,
    TypedMultipart(input::UpdateRtypeInput { rtype }): TypedMultipart<input::UpdateRtypeInput>,
) -> Result<Json<model::RtypeResponse>, crate::Error> {
    let input = service::UpdateRtypeInput { id, rtype };
    let rtype = ctx.rtype_service.update_rtype(input).await?;
    let response = model::RtypeResponse { data: rtype.into() };
    Ok(Json(response))
}

#[utoipa::path(
    delete,
    path = "/rtype/delete/:id",
    responses(
        (status = 204, description = "Delete a rtype", body = RtypeResponse),
    ),
)]
pub async fn delete(
    ctx: Extension<Arc<ServerContext>>,
    Path(id): Path<i64>,
) -> Result<StatusCode, crate::Error> {
    ctx.rtype_service.delete_rtype(id).await?;
    Ok(StatusCode::NO_CONTENT)
}
