pub mod app;

use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, thiserror::Error)]
pub enum Error {
    #[error("Internal error")]
    Internal(String),

    #[error("{0}")]
    NotFound(String),

    #[error("{0}")]
    PermissionDenied(String),

    #[error("{0}")]
    InvalidArgument(String),

    #[error("{0}")]
    AlreadyExists(String),
}

#[derive(Debug, Serialize, Deserialize)]
struct ErrorResponse {
    message: String,
}

// Tell axum how to convert `AppError` into a response.
impl IntoResponse for Error {
    fn into_response(self) -> Response {
        let status_code = match self {
            Error::Internal(_) => StatusCode::INTERNAL_SERVER_ERROR, // 500
            Error::NotFound(_) => StatusCode::NOT_FOUND,             // 404
            Error::InvalidArgument(_) => StatusCode::BAD_REQUEST,    // 400
            Error::AlreadyExists(_) => StatusCode::CONFLICT,         // 409
            Error::PermissionDenied(_) => StatusCode::FORBIDDEN,     // 403
        };

        let err_response = ErrorResponse {
            message: format!("{}", &self),
        };

        (status_code, Json(err_response)).into_response()
    }
}

impl std::convert::From<sqlx::Error> for Error {
    fn from(err: sqlx::Error) -> Self {
        match err {
            sqlx::Error::RowNotFound => Error::NotFound("not found".into()),
            _ => Error::Internal(err.to_string()),
        }
    }
}

impl std::convert::From<std::net::AddrParseError> for Error {
    fn from(err: std::net::AddrParseError) -> Self {
        Error::Internal(err.to_string())
    }
}

impl std::convert::From<std::env::VarError> for Error {
    fn from(err: std::env::VarError) -> Self {
        match err {
            std::env::VarError::NotPresent => Error::NotFound("env var not found".into()),
            _ => Error::Internal(err.to_string()),
        }
    }
}

impl std::convert::From<hyper::Error> for Error {
    fn from(err: hyper::Error) -> Self {
        Error::Internal(err.to_string())
    }
}

impl std::convert::From<axum::http::Error> for Error {
    fn from(err: axum::http::Error) -> Self {
        Error::Internal(err.to_string())
    }
}

impl std::convert::From<tracing_subscriber::filter::ParseError> for Error {
    fn from(err: tracing_subscriber::filter::ParseError) -> Self {
        Error::Internal(err.to_string())
    }
}

impl std::convert::From<tracing_subscriber::filter::FromEnvError> for Error {
    fn from(err: tracing_subscriber::filter::FromEnvError) -> Self {
        Error::Internal(err.to_string())
    }
}

impl std::convert::From<std::num::ParseIntError> for Error {
    fn from(err: std::num::ParseIntError) -> Self {
        Error::InvalidArgument(err.to_string())
    }
}

impl std::convert::From<url::ParseError> for Error {
    fn from(err: url::ParseError) -> Self {
        Error::InvalidArgument(format!("url is not valid: {err}"))
    }
}
