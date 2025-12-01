from bson import ObjectId

def str_to_object_id(id_str: str) -> ObjectId:
    if not ObjectId.is_valid(id_str):
        raise ValueError(f'Invalid ObjectId: {id_str}')
    return ObjectId(id_str)
