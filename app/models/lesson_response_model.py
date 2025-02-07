from pydantic import BaseModel
class TaskDetails(BaseModel):
    type: str
    title: str
    instructions: str
    hint: str
    gpt: str
    
class Task(BaseModel):
    status: str
    task: TaskDetails
    
class StudentResponse(BaseModel):
    task: Task
    latexInput: str
    
class GPTLessonStructedResponse(BaseModel):
    """The overall structured response from GPT for lesson Feedback questions
    -'feedback' -> a Concise string giving feedback for the specific task 
    -'correct' -> a boolean i.e. either true or false, dependent on whether the student was correct or not
    """
    feedback: str
    correct: bool
    
