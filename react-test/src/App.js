import './App.css';
import Header from './myComponent/Header';
import { Footer } from "./myComponent/Footer";
import { Todos } from "./myComponent/Todos";
import { About } from "./myComponent/About";
import React, { useState, useEffect } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";

function App() {
  let initTodo;
  if (localStorage.getItem("Todo") === null) {
    initTodo = [];
  }
  else {
    initTodo = JSON.parse(localStorage.getItem("Todo"))
  }

  const onDelete = (item) => {
    console.log("we wii delete ", item);
    setTodo(Todo.filter((e) => {
      return e != item;
    }))
    localStorage.setItem("Todo", JSON.stringify(Todo));
  }

  const addTodo = (title, desc) => {
    let no;
    if (Todo.length == 0) {
      no = 1;
    } else {
      no = Todo[Todo.length - 1].no + 1;
    }

    console.log("im in add method  ", title, desc, no);

    const myTodo = {
      no: no,
      title: title,
      desc: desc
    }
    setTodo([...Todo, myTodo]);

  }

  const [Todo, setTodo] = useState(initTodo);
  useEffect(() => {
    localStorage.setItem("Todo", JSON.stringify(Todo));
  }, [Todo]);

  return (
    <>
      <Router>
        <Header title="my todos" home/>
        <Routes>
          <Route path="/" element={<Todos todoitems={Todo} onDelete={onDelete} addTodo={addTodo} />} /> 
          <Route path="about/*" element={<About />} />
        </Routes>
        <Footer />
      </Router>
    </>
  );
}

export default App;
