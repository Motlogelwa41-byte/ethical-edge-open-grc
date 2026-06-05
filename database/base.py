from app.database.models import Base

# Explicitly export the base mapping for legacy engine rooms
__all__ = ["Base"]

from sqlalchemy import event
from app.context import current_tenant_id

def apply_tenant_filter(query):
    tenant_id = current_tenant_id.get()
    if tenant_id:
        return query.filter_by(tenant_id=tenant_id)
    return query

# When a query is compiled, SQLAlchemy will automatically inject the tenant_id
@event.listens_for(Query, "before_compile", retval=True)
def before_compile(query):
    if query._setup_args.get("tenant_id_filter", True): # We can toggle this if needed
        return apply_tenant_filter(query)

from sqlalchemy import event
from sqlalchemy.orm import Query
from app.context import current_tenant_id

# This listener intercepts queries before they are sent to the database
@event.listens_for(Query, "before_compile", retval=True)
def apply_tenant_filter(query):
    tenant_id = current_tenant_id.get()
    
    # Only filter if a tenant_id is set in the context
    if tenant_id:
        # Get the classes involved in the query
        for entity in query.column_descriptions:
            model = entity['type']
            # If the model has a tenant_id, filter by it
            if hasattr(model, 'tenant_id'):
                query = query.filter(model.tenant_id == tenant_id)
                
    return query
