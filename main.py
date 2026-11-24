from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Notes API")

class NoteInput(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

notes: list[dict] = []

@app.get("/notes")
def get_all_notes():
    return notes

@app.post("/notes", status_code=201)

def create_note(note: NoteInput):
    new_note = {
        "id": len(notes) + 1,
        "title": note.title,
        "content": note.content,
    }
    notes.append(new_note)
    return new_note

@app.get("/notes/{note_id}")
def get_single_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: NoteInput):
    for note in notes:
        if note["id"] == note_id:
            note["title"] = updated_note.title
            note["content"] = updated_note.content
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    for index, note in enumerate(notes):
        if note["id"] == note_id:
            notes.pop(index)
            return
    raise HTTPException(status_code=404, detail="Note not found")

@app.patch("/notes/{note_id}")
def partial_update_note(note_id: int, note_update: NoteUpdate):
    for note in notes:
        if note["id"] == note_id:
            update_data = note_update.model_dump(exclude_unset=True)
            note.update(update_data)
            return note
    raise HTTPException(status_code=404, detail="Note not found")