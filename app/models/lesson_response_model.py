from pydantic import BaseModel
from typing import List, Dict, Any
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
    # you will need to change the latexInput to be a List[str]
    latexInput: List[str]
    
class GPTLessonStructedResponse(BaseModel):
    """The overall structured response from GPT for lesson Feedback questions
    -'feedback' -> a Concise string giving feedback for the specific task 
    -'correct' -> a boolean i.e. either true or false, dependent on whether the student was correct or not
    """
    feedback: str
    correct: bool

class SelectedChoiceImage(BaseModel):
    url: str
    alt: str
    width: int
    height: int
    isCorrect: bool
    explanation: str
    

class MultipleChoiceImage(BaseModel):
    """The overall structured response from GPT for feedback for lesson questions 
    which are of the multipleChoice image type
    """
    task: Task
    selectedChoice: SelectedChoiceImage
    taskType: str
    
class SketchTaskDetails(BaseModel):
    type: str
    title: str
    instructions: str
    hint: str
    gpt: str
    renderType: str
    marking: dict
    
class SketchTask(BaseModel):
    status: str
    task: SketchTaskDetails
    
    
class Sketch(BaseModel):
    task: SketchTask
    reducedCoordinates: List[Dict[str, float]]
    taskType: str

class SelectedChoice(BaseModel):
    text: str
    isCorrect: bool
    explanation: str
    
class MultipleChoice(BaseModel):
    task: Task
    selectedChoice: SelectedChoice
    taskType: str
    
    

    
class QuestionImageTaskDetails(BaseModel):
    type: str
    title: str
    instructions: str
    hint: str
    gpt: str
    url: str
    alt: str
    caption: str
    latex: str
    renderType: str
    description: str
    markScheme: Dict[str, Any]

    
class QuestionImageTask(BaseModel):
    status: str
    task: QuestionImageTaskDetails
    
class QuestionImage(BaseModel):
    task: QuestionImageTask
    compiledStrings: List[str]
    taskType: str
    

    

    
    
    