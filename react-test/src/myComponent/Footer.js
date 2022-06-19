import React from 'react';


export const Footer = () => {
  let footerDiv = {
    position : "relative",
    width : "100%",
    top :"10vh"
    
  }
  return (
    <div>
      <div className='bg-dark text-light py-3' style={footerDiv}>
        <p className='text-center'>copyright &copy; myTodoList.com</p>
      </div>
    </div>
  )
}

