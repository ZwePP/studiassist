from fastapi import APIRouter

from config.constants import SUBJECTS

router = APIRouter()



@router.get("/subjects")
def get_subjects():
    return {"subjects": SUBJECTS}

