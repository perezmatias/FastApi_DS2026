from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List
from . import schemas, services

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post(
    "/", response_model=schemas.ProductoRead, status_code=status.HTTP_201_CREATED
)
def alta_producto(producto: schemas.ProductoCreate):
    return services.crear(producto)

@router.get(
    "/", response_model=List[schemas.ProductoRead], status_code=status.HTTP_200_OK
)
def listar_productos(skip: int = Query(0, ge=0), limit: int = Query(10, le=50)):
    return services.obtener_todos(skip, limit)

@router.get(
    "/{id}", response_model=schemas.ProductoRead, status_code=status.HTTP_200_OK
)
def detalle_producto(id: int = Path(..., gt=0)):
    producto = services.obtener_por_id(id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return producto

@router.put(
    "/{id}", response_model=schemas.ProductoRead, status_code=status.HTTP_200_OK
)
def actualizar_producto(producto: schemas.ProductoCreate, id: int = Path(..., gt=0)):
    actualizado = services.actualizar_total(id, producto)
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return actualizado

@router.put(
    "/{id}/desactivar",
    response_model=schemas.ProductoRead,
    status_code=status.HTTP_200_OK,
)
def borrado_logico(id: int = Path(..., gt=0)):
    desactivado = services.desactivar(id)
    if not desactivado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return desactivado

@router.get(
    "/{id}/stock",
    response_model=schemas.ProductoStockResponse,
    status_code=status.HTTP_200_OK,
)
@router.get("/{id}/stock", response_model=schemas.ProductoStockResponse)
def consultar_stock(id: int = Path(..., gt=0)):
    resultado = services.obtener_estado_stock(id)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
        )
    return resultado
