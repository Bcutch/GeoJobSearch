import React, { useState, useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import NotesList from './components/NotesList';
import NewNoteForm from './components/NewNoteForm';
import ErrorAlert from '../../components/ErrorAlert';
import LoadingSpinner from '../../components/LoadingSpinner';
import EditNoteModal from './components/EditNoteModal';
import GlobalNavBar from '../../components/GlobalNavBar';


const HomePage = () => {
    const [notes, setNotes] = useState([]);
    const [count, setCount] = useState(0);
    const [newNote, setNewNote] = useState('');
    const [showEdit, setShowEdit] = useState(false);
    const [noteToEdit, setNoteToEdit] = useState(null);
    const [loading, setLoading] = useState(false);
    const [loadingCount, setLoadingCount] = useState(false);
    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState(null);

    useEffect(() => {
        fetchCount();
        fetchAllNotes();
    }, [])


    const status = (res) => {
        if (!res.ok) {
            throw new Error('Something Went Wrong');
        }
        return res;
    }

    const fetchAllNotes = () => {
        setLoading(true);
        fetch('/api/notes/all')
            .then(status)
            .then(res => res.json())
            .then(data => {
                setNotes(data);
                setLoading(false);
            }).catch(error => {
                setErrorMessage(error.message);
                setError(true);
            });
    }

    const fetchCount = () => {
        setLoadingCount(true);
        fetch('/api/notes/count')
            .then(status)
            .then(res => res.json())
            .then(data => {
                setCount(data);
                setLoadingCount(false);
            }).catch(error => {
                setErrorMessage(error.message);
                setError(true);
            });
    }

    const addNewNote = () => {
        fetch('/api/notes/add', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                text: newNote
            })
        })
        .then(status)
        .then(res => {
            console.log(res);
            setNewNote('');
            fetchAllNotes();
            fetchCount();
        }).catch(error => {
            setErrorMessage(error.message);
            setError(true);
        });
    }

    const deleteNote = (id) => {
        fetch(`/api/notes/delete/${id}`, {
            method: 'DELETE'
        })
        .then(status)
        .then(res => {
            console.log(res);
            fetchAllNotes();
            fetchCount();
        }).catch(error => {
            setErrorMessage(error.message);
            setError(true);
        });
    }

    const triggerEditModal = (note) => {
        setNoteToEdit(note);
        setShowEdit(true);
    }

    const editClose = () => {
        setShowEdit(false);
    }

    const editNote = (note) => {
        fetch('/api/notes/update', {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(note)
        })
        .then(status)
        .then(res => {
            console.log(res);
            fetchAllNotes();
        }).catch(error => {
            setErrorMessage(error.message);
            setError(true);
        });
    }

    return(
        <div>
            <GlobalNavBar pageName='Home'/>
            <Container>
                {error ? 
                    <ErrorAlert errorMessage={errorMessage} onClose={() => setError(false)} />
                    :
                    <div></div>
                }
                <NewNoteForm value={newNote} onChange={setNewNote} onSubmit={addNewNote} />
                <br />
                {loading || loadingCount ? 
                    <LoadingSpinner />
                    : 
                    <div>
                        <NotesList list={notes} count={count} onEdit={triggerEditModal} onDelete={deleteNote}/>
                    </div>
                }
            </Container>
            <EditNoteModal note={noteToEdit} show={showEdit} onClose={editClose} onSave={editNote} />
        </div>
    )
}

export default HomePage;