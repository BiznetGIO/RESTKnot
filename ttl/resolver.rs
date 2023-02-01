use std::sync::Arc;

use async_graphql::{Context, Error, FieldResult, Object};

use super::{model, service};
use crate::{context::ServerContext, scalar::Id};

#[derive(Default)]
pub struct TtlQuery;

#[Object]
impl TtlQuery {
    pub async fn ttls(
        &self,
        ctx: &Context<'_>,
        first: Option<i32>,
        after: Option<String>,
        last: Option<i32>,
        before: Option<String>,
    ) -> FieldResult<model::TtlConnection> {
        let server_ctx = ctx.data::<Arc<ServerContext>>()?;
        let ttl_edges = server_ctx
            .ttl_service
            .find_ttls(first, after.as_deref(), last, before.as_deref())
            .await?;
        let edges: Vec<model::TtlEdge> = ttl_edges.into_iter().map(|ttl| ttl.into()).collect();

        let ttl_connection = model::TtlConnection {
            edges,
            //
            after,
            before,
            first,
            last,
        };

        Ok(ttl_connection)
    }
    pub async fn ttl(&self, ctx: &Context<'_>, id: Id) -> FieldResult<model::Ttl> {
        let server_ctx = ctx.data::<Arc<ServerContext>>()?;

        let result = server_ctx.ttl_service.find_ttl(id).await;
        match result {
            Ok(res) => Ok(res.into()),
            Err(err) => Err(Error::new(err.to_string())),
        }
    }
}

#[derive(Default)]
pub struct TtlMutation;

#[Object]
impl TtlMutation {
    pub async fn create_ttl(
        &self,
        ctx: &Context<'_>,
        input: model::input::CreateTtlInput,
    ) -> FieldResult<model::Ttl> {
        let server_ctx = ctx.data::<Arc<ServerContext>>()?;

        let service_input = service::CreateTtlInput { time: input.time };
        let result = server_ctx.ttl_service.create_ttl(service_input).await;
        match result {
            Ok(res) => Ok(res.into()),
            Err(err) => Err(Error::new(err.to_string())),
        }
    }
    pub async fn update_ttl(
        &self,
        ctx: &Context<'_>,
        input: model::input::UpdateTtlInput,
    ) -> FieldResult<model::Ttl> {
        let server_ctx = ctx.data::<Arc<ServerContext>>()?;

        let service_input = service::UpdateTtlInput {
            id: input.id,
            time: input.time,
        };
        let result = server_ctx.ttl_service.update_ttl(service_input).await;
        match result {
            Ok(res) => Ok(res.into()),
            Err(err) => Err(Error::new(err.to_string())),
        }
    }
    pub async fn delete_ttl(&self, ctx: &Context<'_>, id: Id) -> FieldResult<model::Ttl> {
        let server_ctx = ctx.data::<Arc<ServerContext>>()?;

        let result = server_ctx.ttl_service.delete_ttl(id).await;
        match result {
            Ok(res) => Ok(res.into()),
            Err(err) => Err(Error::new(err.to_string())),
        }
    }
}
