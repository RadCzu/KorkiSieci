import sys
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Application state stored in memory
app_state = {"text": "DOMYŚLNY TEKST"}


# Data structure for the incoming payload
class NewText(BaseModel):
  text: str


# GET endpoint: Retrieve the current text
@app.get("/")
def get_text():
  return {
      "message": app_state["text"],
      "info": "To jest obecny tekst zapisany w pamięci",
  }


# POST endpoint: Update the text on the server
@app.post("/update")
def update_text(data: NewText):
  old_text = app_state["text"]
  app_state["text"] = data.text
  return {
      "status": "success",
      "before_change": old_text,
      "after_change": app_state["text"],
  }


if __name__ == "__main__":
  port = 8000
  if len(sys.argv) > 1:
    try:
      port = int(sys.argv[1])
    except ValueError:
      print("Port must be a number! Running on default 8000.")

  print(f"--- Starting server on port {port} ---")
  uvicorn.run(app, host="127.0.0.1", port=port)