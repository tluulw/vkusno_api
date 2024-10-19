from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.items.models import item
from src.items.schemas import ItemAdd
from src.items.utils import items_serialize

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@router.post("/add")
async def add_item(new_item: ItemAdd, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(item).values(new_item.model_dump())
    await session.execute(stmt)

    await session.commit()

    return {"status_code": 201, "details":
            {"message": "Item was added"}
            }


@router.post("/add/many")
async def add_many_items(new_positions: list[dict], session: AsyncSession = Depends(get_async_session)):
    stmt_for_all_ids = select(item)
    request = await session.execute(stmt_for_all_ids)

    result = request.scalars().all()  # getting all id's

    last_id = result[-1] if len(result) else 0

    new_items = await items_serialize(new_positions, last_id)

    stmt_for_add = insert(item).values([position.model_dump() for position in new_items])
    await session.execute(stmt_for_add)

    await session.commit()

    return {"status_code": 201, "details": {
        "message": "Items was added"}
            }
