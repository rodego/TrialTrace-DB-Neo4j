import logo from './logo.svg';
import './App.css';
import Login from "./components/Login"
import Logout from "./components/Logout"
import { useAuth0 } from "@auth0/auth0-react";

// fonts
import "@fontsource/roboto/300.css"
import "@fontsource/roboto/400.css"
import "@fontsource/roboto/500.css"
import "@fontsource/roboto/700.css"

function App() {

const { user, isAuthenticated, isLoading } = useAuth0()

  return (
    <div className="App">
        {/* {isAuthenticated ? <Logout /> : <Login />} */}
    </div>
  );
}

export default App;