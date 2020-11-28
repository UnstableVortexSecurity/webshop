from flask_security import current_user
from models import db, Purchase, Item


def user_can_access_caff(item: Item) -> bool:
    if not current_user.is_authenticated:
        return False
    else:

        if item.uploader == current_user:
            return True
        else:
            p = Purchase.query.filter(
                db.and_(Purchase.purchaser_id == current_user.id, Purchase.item_id == item.id)).first()
            return bool(p)
