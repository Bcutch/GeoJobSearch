package com.example.cis4900.spring.template.notes;

import com.example.cis4900.spring.template.notes.models.Note;


public interface NotesService {
    public String addNote(Note newNote);

    public Note getNote(Integer id);
    
    public String updateNote(Note updatedNote);

    public String deleteNote(Integer id);

    public Iterable<Note> allNotes();

    public Integer count();
}
