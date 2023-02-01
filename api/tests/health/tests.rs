use anyhow::Result;
use api::routes::app;
use axum::{
    body::Body,
    http::{Request, StatusCode},
};
use tower::util::ServiceExt;

use super::schema::HealthResponse;

#[tokio::test]
async fn health() -> Result<()> {
    let app = app().await?;

    let request = Request::builder().uri("/health").body(Body::empty())?;

    let response = app.oneshot(request).await?;
    assert_eq!(response.status(), StatusCode::OK);

    let body = hyper::body::to_bytes(response.into_body()).await?;
    let body: HealthResponse = serde_json::from_slice(&body)?;
    assert_eq!(body.data.status, "running");
    Ok(())
}
