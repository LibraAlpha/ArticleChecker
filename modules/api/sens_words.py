from fastapi import APIRouter, Request
from modules import sensitive_words_tools as processor
from configs import action_code

router = APIRouter()


@router.get('/api/sensitive-words/list')
async def get_sensitive_words(page_index: int, page_limit: int):
    ret = processor.load(page_index, page_limit)
    return ret


@router.post('/api/sensitive-words/find')
async def get_sensitive_word(word: str):
    ret = processor.find_sensitive_word(word)
    return ret


@router.post('/api/sensitive-words/add')
async def add(word: str):
    ret = processor.add_sensitive_word(word)
    return ret


@router.delete("/sensitive-words/del")
async def delete_sensitive_word(word: str):
    # 处理删除敏感词的逻辑
    ret = processor.remove(word)
    return ret
