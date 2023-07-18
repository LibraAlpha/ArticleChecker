from fastapi import APIRouter, Request
from modules import sensitive_words_tools as processor
from configs import action_code

router = APIRouter()


@router.get('/api/sensitive-words/list')
async def get_sensitive_words(page_index: int, page_limit: int):
    ret = processor.load(page_index, page_limit)
    return ret


@router.get('/api/sensitive-words/size')
async def get_size():
    return processor.get_size()


@router.post('/api/sensitive-words/find')
async def get_sensitive_word(word: str):
    word_set = processor.find_sensitive_word(word)
    return word_set


@router.post('/api/sensitive-words/add')
async def add(word: str):
    ret = processor.add_sensitive_word(word)
    if action_code.WORD_INSERT_SUCCESS == ret:
        return {"message": f"Add sensitive word: {word}"}


@router.delete("/sensitive-words/del")
async def delete_sensitive_word(word: str):
    # 处理删除敏感词的逻辑
    ret = processor.remove_word_from_sensitive_list(word)
    if action_code.WORD_DEL_SUCCESS == ret:
        return {"message": f"Deleted sensitive word: {word}"}
