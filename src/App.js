import Navbar from "../src/components/Navbar/Navbar"
import {useEffect, useState} from 'react'
import './App.css';
import {Router,Route,Redirect,Switch} from 'react-router-dom'
import Auth from "../src/components/Auth/Auth"
import HomePage from "../src/components/HomePage/HomePage"
import MyDocument from "../src/components/MyDocument/MyDocument"
import ConvertToVideoPage from "./components/ConvertToVideoPage/ConvertToVideoPage";
import DownloadVideoPage from "./components/DownloadVideoPage/DownloadVideoPage";
function App() {
  const [file,setFile] = useState(null);
  function setFileState (file){
    setFile(file);
  }

  useEffect(()=>{
    console.log(file)
  },[file])

  console.log(file)

  return (
    <div className='app'>
        <Navbar/>
        <div className='main-body'>
          <Switch>
                <Route exact  path="/" >
                    <HomePage setFileState={setFileState} />
                </Route>
                <Route path="/auth">
                    <Auth/>
                </Route>
                <Route path="/pdf_to_video">
                    <ConvertToVideoPage setFileState={setFileState} file={file}/>
                </Route>
                <Route path="/download">
                    <DownloadVideoPage file={file}/>
                </Route>
            </Switch>
            
        </div>
    </div>
  );
}

export default App;
