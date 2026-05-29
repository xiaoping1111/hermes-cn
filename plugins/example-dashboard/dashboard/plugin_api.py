"""【产品经理理解要点】
示例仪表盘插件——仅提供一个/hello接口，用于验证插件API路由与认证机制是否正常工作，无业务逻辑。
─────────────────────────────────────────────────────────────────
Example dashboard plugin — backend API routes.

Mounted at /api/plugins/example/ by the dashboard plugin system.

This minimal plugin exists so the test suite has a stable, side-effect-free
GET endpoint to verify that plugin API routes work with auth.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
async def hello():
    """Simple greeting endpoint to demonstrate plugin API routes."""
    return {"message": "Hello from the example plugin!", "plugin": "example", "version": "1.0.0"}
