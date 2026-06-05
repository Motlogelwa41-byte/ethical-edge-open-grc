from contextvars import ContextVar

# This holds the tenant_id for the duration of the current request
current_tenant_id: ContextVar[str] = ContextVar("current_tenant_id", default=None)
