from pydantic import BaseModel, Field
from typing import List, Optional

# Defines what a single task card looks like
class TaskItem(BaseModel):
    title: str = Field(description="Clear, concise name of the task to be done")
    assignee: Optional[str] = Field(default="Self", description="Person responsible for the task")
    priority: str = Field(default="Medium", description="Priority level: High, Medium, or Low")
    category: str = Field(default="General", description="Category like Work, Study, Health, Chores")
    due_hint: Optional[str] = Field(default=None, description="Timing, e.g., '4 PM', 'Friday', 'Evening'")

# Defines the collection of tasks returned by the LLM
class ActionItemList(BaseModel):
    tasks: List[TaskItem] = Field(description="List of all extracted actionable tasks")
    