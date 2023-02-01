use std::sync::Arc;

use axum::response::IntoResponse;
use axum::{extract::Path, http::StatusCode, response::Response, Extension, Json};
use axum_typed_multipart::TypedMultipart;

use super::model::input;
use super::{model, service};
use crate::context::ServerContext;

// utoipa can't find `model::<StructName>`
#[allow(unused_imports)]
use crate::user::model::User;

#[utoipa::path(
    get,
    path = "/user/list",
    responses(
        (status = 200, description = "List all users", body = UsersResponse),
    ),
)]
pub async fn list(
    ctx: Extension<Arc<ServerContext>>,
) -> Result<Json<model::UsersResponse>, crate::Error> {
    let users = ctx.user_service.find_users().await?;

    let users = users.into_iter().map(|t| t.into()).collect();
    let response = model::UsersResponse { data: users };
    Ok(Json(response))
}

#[utoipa::path(
    get,
    path = "/user/list/:id",
    responses(
        (status = 200, description = "Get a user by id", body = UserResponse),
    ),
)]
pub async fn get(
    ctx: Extension<Arc<ServerContext>>,
    Path(id): Path<i64>,
) -> Result<Json<model::UserResponse>, crate::Error> {
    let user = ctx.user_service.find_user(id).await?;

    let response = model::UserResponse { data: user.into() };
    Ok(Json(response))
}

#[utoipa::path(
    post,
    path = "/user/add",
    responses(
        (status = 201, description = "Create new user", body = UserResponse),
    ),
)]
pub async fn post(
    ctx: Extension<Arc<ServerContext>>,
    TypedMultipart(input::CreateUserInput { email }): TypedMultipart<input::CreateUserInput>,
) -> Result<Response, crate::Error> {
    let input = service::CreateUserInput { email };
    let user = ctx.user_service.create_user(input).await?;
    let response = model::UserResponse { data: user.into() };
    Ok((StatusCode::CREATED, Json(response)).into_response())
}

#[utoipa::path(
    put,
    path = "/user/edit/:id",
    responses(
        (status = 200, description = "Update a user", body = UserResponse),
    ),
)]
pub async fn put(
    ctx: Extension<Arc<ServerContext>>,
    Path(id): Path<i64>,
    TypedMultipart(input::UpdateUserInput { email }): TypedMultipart<input::UpdateUserInput>,
) -> Result<Json<model::UserResponse>, crate::Error> {
    let input = service::UpdateUserInput { id, email };
    let user = ctx.user_service.update_user(input).await?;
    let response = model::UserResponse { data: user.into() };
    Ok(Json(response))
}

#[utoipa::path(
    delete,
    path = "/user/delete/:id",
    responses(
        (status = 204, description = "Delete a user", body = UserResponse),
    ),
)]
pub async fn delete(
    ctx: Extension<Arc<ServerContext>>,
    Path(id): Path<i64>,
) -> Result<StatusCode, crate::Error> {
    ctx.user_service.delete_user(id).await?;
    Ok(StatusCode::NO_CONTENT)
}
