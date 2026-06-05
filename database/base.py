from sqlalchemy import event
from sqlalchemy.orm import Query
from app.database.models import Base
from app.context import current_tenant_id

# Export the Base
__all__ = ["Base"]

@event.listens_for(Query, "before_compile", retval=True)
def apply_tenant_filter(query):
    """
    Automatic security filter: Intercepts all queries and 
    injects the tenant_id if the model supports multi-tenancy.
    """
    tenant_id = current_tenant_id.get()
    
    # Only apply filter if we have a valid tenant in context
    if tenant_id:
        for entity in query.column_descriptions:
            model = entity['type']
            # Only filter if the model has a tenant_id attribute
            if model and hasattr(model, 'tenant_id'):
                query = query.filter(model.tenant_id == tenant_id)
    
    return query
