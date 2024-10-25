from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["products"],)
@router.get("/")
async def products():
    return ["Producto 1", "Producto 1", "Producto 1", "Producto 1",]