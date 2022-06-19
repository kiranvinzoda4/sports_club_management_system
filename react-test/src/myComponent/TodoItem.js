import React from 'react'

export const TodoItem = ({item, onDelete}) => {
  return (
    <div className='my-3'>
        <h4>
           {item.no} {item.title} 
        </h4>
        <p>
        {item.desc}
        </p>
        <button className='btn btn-sm btn-danger' onClick={()=>{onDelete(item)}}>delete</button>
        <hr/>
    </div>
  )
}
