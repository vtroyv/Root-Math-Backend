from fastapi import FastAPI, APIRouter
from ..models.tutor_models import PromptResponse



app = FastAPI()
router = APIRouter(prefix='/ask-tutor')

@router.post("/")
async def ask_tutor(prompt: PromptResponse):
# Now that we can sucessfully obtain the prompt it's time to connect it to gpt 
# In addition it may be especially wise to also collect state data from the question/lesson and use this to help prompt engineer/ provide context 
#
    return {"prompt": prompt}
