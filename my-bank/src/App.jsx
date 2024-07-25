import 'bootstrap/dist/css/bootstrap.min.css';
import BankNavbar from './Components/Navbar';
import { BrowserRouter,Route,Routes } from 'react-router-dom';
import Footer from './Components/Footer';
import SuperadminLogin from './Components/AdminLogin';
import CustomerRegistration from './Components/Userregister';
import CustomerLogin from './Components/Userlogin';
import TransferFunds from './Components/Home';
import Transaction from './Components/Transaction';
import LoanApplication from './Components/Loanapply';
// import AdminLoanManagement from './Components/Adminmanage';
import PasswordChange from './Components/password';
import Loanmanage from './Components/Adminmanage';





function App() {


  return (
    <>
     <div className="App">
      <BankNavbar />
      <Routes>
      <Route path='/' element={<SuperadminLogin/>}/>
      <Route path='/login' element={<SuperadminLogin/>}/>
      <Route path='/register' element={<CustomerRegistration/>}/>
      <Route path='/user' element={<CustomerLogin/>}/>
      <Route path='/transfer' element={<TransferFunds/>}/>
      <Route path='/transaction' element={<Transaction/>}/>
      <Route path='/loan' element={<LoanApplication/>}/>
      <Route path='/permission' element={<Loanmanage/>}/>
      <Route path='/password' element={<PasswordChange/>}/>
      </Routes>
      <Footer />
    </div>
     
    </>
  );
}

export default App
