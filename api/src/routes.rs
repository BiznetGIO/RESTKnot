use std::sync::Arc;

use axum::{
    routing::{delete, get, post, put},
    Extension, Router,
};
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

use crate::{config, context::ServerContext, db, health, meta, record, rtype, ttl, user};

pub async fn app() -> Result<Router, crate::Error> {
    let config = Arc::new(config::Config::load()?);
    let db = db::connect(&config.database).await?;

    let health_service = Arc::new(health::Service::new());
    let meta_service = Arc::new(meta::Service::new(config.clone()));
    let ttl_service = Arc::new(ttl::Service::new(db.clone()));
    let rtype_service = Arc::new(rtype::Service::new(db.clone()));
    let user_service = Arc::new(user::Service::new(db.clone()));
    let record_service = Arc::new(record::Service::new(
        db,
        rtype_service.clone(),
        ttl_service.clone(),
    ));
    let server_context = Arc::new(ServerContext {
        health_service,
        meta_service,
        ttl_service,
        rtype_service,
        user_service,
        record_service,
    });

    #[derive(OpenApi)]
    #[openapi(
        paths(
            meta::query::version,
            meta::query::config,
            health::query::health,
            ttl::query::list, ttl::query::get, ttl::query::post, ttl::query::put, ttl::query::delete,
            rtype::query::list, rtype::query::get, rtype::query::post, rtype::query::put, rtype::query::delete,
            user::query::list, user::query::get, user::query::post, user::query::put, user::query::delete,
            record::query::list, record::query::get, record::query::post
        ),
        components(schemas(
            meta::model::Version, meta::model::VersionResponse, meta::model::Config, meta::model::ConfigResponse,
            health::model::Health, health::model::HealthResponse,
            ttl::model::Ttl, ttl::model::TtlsResponse, ttl::model::TtlsResponse,
            rtype::model::Rtype, rtype::model::RtypesResponse, rtype::model::RtypeResponse,
            user::model::User, user::model::UsersResponse, user::model::UserResponse,
            record::model::Record, record::model::RecordsResponse, record::model::RecordResponse,
        )),
        tags(
            (name = "RESTKnot", description = "RESTKnot REST API")
        )
    )]
    struct ApiDoc;

    let mut app = Router::new()
        .route("/health", get(health::query::health))
        // meta
        .route("/meta/version", get(meta::query::version))
        .route("/meta/config", get(meta::query::config))
        // ttl
        .route("/ttl/list", get(ttl::query::list))
        .route("/ttl/list/:id", get(ttl::query::get))
        .route("/ttl/add", post(ttl::query::post))
        .route("/ttl/edit/:id", put(ttl::query::put))
        .route("/ttl/delete/:id", delete(ttl::query::delete))
        // rtype
        .route("/type/list", get(rtype::query::list))
        .route("/type/list/:id", get(rtype::query::get))
        .route("/type/add", post(rtype::query::post))
        .route("/type/edit/:id", put(rtype::query::put))
        .route("/type/delete/:id", delete(rtype::query::delete))
        // user
        .route("/user/list", get(user::query::list))
        .route("/user/list/:id", get(user::query::get))
        .route("/user/add", post(user::query::post))
        .route("/user/edit/:id", put(user::query::put))
        .route("/user/delete/:id", delete(rtype::query::delete));
    // record
    // .route("/record/list", get(record::query::list))
    // .route("/record/list/:id", get(record::query::get))
    // .route("/record/add", post(record::query::post))
    // .route("/record/edit/:id", put(record::query::put))
    // .route("/record/delete/:id", delete(rtype::query::delete));

    if config.env != config::Env::Production {
        app = app.merge(SwaggerUi::new("/swagger").url("/api-doc/openapi.json", ApiDoc::openapi()));
    }
    let app = app.layer(Extension(server_context));

    Ok(app)
}
