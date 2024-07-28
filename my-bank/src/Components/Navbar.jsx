import React,{ useEffect} from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Navbar.css';

function BankNavbar({isLoggedIn,setIsLoggedIn}) {
  
  const navigate=useNavigate();

  useEffect(() => {
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      setIsLoggedIn(true);
    }
  }, [setIsLoggedIn]);

  const handleLogout = async  () => {
    try {
      const accessToken = localStorage.getItem('accessToken');

      await axios.post('http://127.0.0.1:8000/customerlogout/', {}, {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      });




    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('customerEmail');
    localStorage.removeItem('customerPassword');
    localStorage.removeItem('loggedInUsername');
    setIsLoggedIn(false);
    navigate('/user');
  } catch (error) {
    console.error('Logout error:', error);
  }
};










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
        {isLoggedIn ? (
            <Nav.Link onClick={handleLogout}>Logout</Nav.Link>
          ) : (
            <Nav.Link href="/user">Login</Nav.Link>
          )}
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default BankNavbar;



