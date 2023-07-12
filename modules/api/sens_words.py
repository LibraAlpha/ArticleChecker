from fastapi import APIRouter, Request
from modules import sensitive_words_tools as processor
from configs import action_code

router = APIRouter()


@router.get('/api/sensitive-words')
async def get_sensitive_words():
    ret = processor.load_all()
    return ret


@router.post('/api/sensitive-words/{word}/')
async def get_sensitive_word(word: str):
    word_set = processor.find_sensitive_word(word)
    return word_set


@router.post('/api/sensitive-words/')
async def add(word: str):
    ret = processor.add_sensitive_word(word)
    if action_code.WORD_INSERT_SUCCESS == ret:
        return {"message": f"Add sensitive word: {word}"}


@router.delete("/sensitive-words/{word}")
async def delete_sensitive_word(word: str):
    # 处理删除敏感词的逻辑
    ret = processor.remove_word_from_sensitive_list(word)
    if action_code.WORD_DEL_SUCCESS == ret:
        return {"message": f"Deleted sensitive word: {word}"}
