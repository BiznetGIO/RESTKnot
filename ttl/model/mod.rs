pub mod input;

use std::sync::Arc;

use async_graphql::{ComplexObject, Context, Result, SimpleObject};

use crate::{context::ServerContext, relay, scalar::Id, ttl::entities};

#[derive(Debug, SimpleObject)]
pub struct Ttl {
    /// The ID of the ttl.
    pub id: Id,
    /// The time for the ttl.
    pub time: i32,
}

impl From<entities::Ttl> for Ttl {
    fn from(t: entities::Ttl) -> Self {
        Self {
            id: t.id,
            time: t.time,
        }
    }
}

#[derive(Debug, SimpleObject)]
#[graphql(complex)]
/// The connection type for ttl.
pub struct TtlConnection {
    /// A list of edges.
    pub edges: Vec<TtlEdge>,
    //
    // helper
    //
    #[graphql(skip)]
    /// Returns the elements in the list that come after the specified cursor.
    pub after: Option<String>,
    #[graphql(skip)]
    pub before: Option<String>,
    #[graphql(skip)]
    pub first: Option<i32>,
    #[graphql(skip)]
    pub last: Option<i32>,
}

#[derive(Debug, SimpleObject)]
pub struct TtlEdge {
    /// The item at the end of the edge.
    pub node: Ttl,
    /// A cursor for use in pagination.
    pub cursor: String,
}

#[ComplexObject]
impl TtlConnection {
    /// Information to aid in pagination.
    async fn page_info(&self, ctx: &Context<'_>) -> Result<relay::PageInfo> {
        let ctx = ctx.data::<Arc<ServerContext>>()?;
        let conn = relay::Connection::new(ctx.clone());

        let page_info = conn
            .page_info(
                self.first,
                self.after.as_deref(),
                self.last,
                self.before.as_deref(),
            )
            .await?;
        Ok(page_info)
    }
    /// Identifies the total count of items in the connection.
    async fn total_count(&self, ctx: &Context<'_>) -> Result<i64> {
        let ctx = ctx.data::<Arc<ServerContext>>()?;
        let conn = relay::Connection::new(ctx.clone());
        Ok(conn.total_count("ttl").await?)
    }
}

impl From<entities::TtlEdge> for TtlEdge {
    fn from(t: entities::TtlEdge) -> Self {
        Self {
            node: t.node.into(),
            cursor: t.cursor,
        }
    }
}

impl From<entities::Ttl> for TtlEdge {
    fn from(t: entities::Ttl) -> Self {
        let cursor = relay::Base64Cursor::new(t.id).encode();
        let ttl_model = t.into();
        Self {
            node: ttl_model,
            cursor,
        }
    }
}
