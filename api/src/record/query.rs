use std::sync::Arc;

use axum::response::IntoResponse;
use axum::{extract::Path, http::StatusCode, response::Response, Extension, Json};
use axum_typed_multipart::TypedMultipart;

use super::model::input;
use super::{model, service};
use crate::context::ServerContext;

// utoipa can't find `model::<StructName>`
#[allow(unused_imports)]
use crate::record::model::Record;

#[utoipa::path(
    get,
    path = "/record/list",
    responses(
        (status = 200, description = "List all records", body = RecordsResponse),
    ),
)]
pub async fn list(
    ctx: Extension<Arc<ServerContext>>,
) -> Result<Json<model::RecordsResponse>, crate::Error> {
    let records = ctx.record_service.find_records().await?;

    let records = records.into_iter().map(|t| t.into()).collect();
    let response = model::RecordsResponse { data: records };
    Ok(Json(response))
}

#[utoipa::path(
    get,
    path = "/record/list/:id",
    responses(
        (status = 200, description = "Get a record by id", body = RecordResponse),
    ),
)]
pub async fn get(
    ctx: Extension<Arc<ServerContext>>,
    Path(id): Path<i64>,
) -> Result<Json<model::RecordResponse>, crate::Error> {
    let record = ctx.record_service.find_record(id).await?;

    let response = model::RecordResponse {
        data: record.into(),
    };
    Ok(Json(response))
}

#[utoipa::path(
    post,
    path = "/record/add",
    responses(
        (status = 201, description = "Create new record", body = RecordResponse),
    ),
)]
pub async fn post(
    ctx: Extension<Arc<ServerContext>>,
    TypedMultipart(input::CreateRecordInput {
        zone,
        owner,
        rtype,
        rdata,
        ttl,
    }): TypedMultipart<input::CreateRecordInput>,
) -> Result<Response, crate::Error> {
    let input = service::CreateRecordInput {
        zone,
        owner,
        rtype,
        rdata,
        ttl,
    };
    let record = ctx.record_service.create_record(input).await?;
    let response = model::RecordResponse {
        data: record.into(),
    };
    Ok((StatusCode::CREATED, Json(response)).into_response())
}
