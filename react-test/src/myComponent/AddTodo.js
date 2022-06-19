
import React, { useState } from 'react';

export const AddTodo = ({addTodo}) => {

    const [title , setTitle] = useState("");
    const [desc, setDesc] = useState("");
    const submit = (e)=>{
        e.preventDefault();
        if(!title || !desc){
            alert("dont leave title or desc blank");
        }else{
            addTodo(title, desc);
        }
        setDesc("");
        setTitle("");
    }
    return (
        <div className='my-3'>
            <form onSubmit={submit}>
                <div className="form-group my-3" >
                    <label htmlFor="title">title</label>
                    <input type="text" className="form-control" onChange={(e)=>setTitle(e.target.value)} value={title} id="title" aria-describedby="emailHelp" placeholder="title" />
                </div>
                <div className="form-group my-3">
                    <label htmlFor="desc">description</label>
                    <input type="text" className="form-control" onChange={(e)=>setDesc(e.target.value)} value={desc} id="desc" placeholder="description" />
                </div>
                <button type="submit" className="btn btn-sm btn-success my-3">Submit</button>
            </form>
        </div>
    )
}
