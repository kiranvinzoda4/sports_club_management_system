import React from 'react'
import { TodoItem } from "./TodoItem";
import { AddTodo } from "./AddTodo";

export const Todos = (props) => {
  return (
    <div className='container'>
      <h4 className='text-center my-3'>todos</h4>
      <div className='row'>
        <div className='col-sm-6'>
          <h5>Todo list</h5>
          { props.todoitems===null ? "todo list is empty" :
            props.todoitems.map((item) => {
              return <TodoItem item={item} key={item.no} onDelete={props.onDelete} />
            })}
        </div>
        <div className='col-sm-6'>
          <h5>Add todo in list</h5>
          <AddTodo addTodo = {props.addTodo}/>
        </div>
      </div>
    </div>

  )
}

