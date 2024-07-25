import React, { useState } from 'react';
import { Link,useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Userlogin.css';


const CustomerLogin = () => {
  const [email, setEmail] = useState();
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:8000/customerlogin/', {
        email: email,
        password: password,
      
      });
      console.log(response);
     
      if (response.status === 200){
        
            localStorage.setItem('accessToken', response.data.access);
            localStorage.setItem('email', response.data.email);
            localStorage.setItem('loggedInUsername',response.data.username);
            navigate('/transaction')
            console.log('Login successful:', response.data);
        } else {
              console.error('error', response.data.message)
          }
      

    } catch (error) {
      setError('Invalid email or password.'); // Handle error responses
      console.error('Login error:', error);
    }
  };

  return (
    <div className="login-container">
    <div className="login-form">
      <h2 className="text-center mb-4">Customer Login</h2>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleLogin}>
        <div className="mb-3">
          <label htmlFor="username" className="form-label">Email:</label>
          <input
            type="email"
            id="email"
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label htmlFor="password" className="form-label">Password:</label>
          <input
            type="password"
            id="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button className='btn btn-primary'>Login</button>
      </form>
    </div>
  </div>
  );
};

export default CustomerLogin;
