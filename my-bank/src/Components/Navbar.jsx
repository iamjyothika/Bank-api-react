import React from 'react';
import { Navbar, Nav, NavDropdown, Form, FormControl, Button } from 'react-bootstrap';
import './Navbar.css';

function BankNavbar() {
  return (
    <Navbar bg="orange" expand="lg">
      <Navbar.Brand href="#home">Bank</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link href='/'>Home</Nav.Link>
          <Nav.Link href='/login'>Admin Login</Nav.Link>
          
        </Nav>

        <Nav>
          <Nav.Link href="/user">Login</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default BankNavbar;



