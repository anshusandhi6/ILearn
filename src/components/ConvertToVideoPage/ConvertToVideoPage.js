import React,{useState,useEffect} from 'react'
import MyDocument from '../MyDocument/MyDocument'
import './ConvertToVideoPage.css'
import {history} from '../../helpers/history'
import axios from 'axios'
import Popup from '../Popup/Popup'
import LoaderCustom from '../Loader/Loader'
const ConvertToVideoPage = (props) => {


    const [showPopUp,setShowPopUp] = useState(false)
    const [language,setLanguage] = useState('english')
    const [speed,setSpeed] = useState('1')
    const [loader,setLoader] = useState(false);
    const handleLanguageChange = (e)=>{
        setLanguage(e.target.value); 
    }

    useEffect(()=>{
        console.log('hello re rendering force fully')
    })

    console.log('is being re redered')

    const handleSpeedChange = (e)=>{
        setSpeed(e.target.value); 
    }

    console.log(language);
    console.log(speed);
    const onClickHandler = (e)=>{
        e.preventDefault();
        // const formData = new FormData();
        // formData.append("file", props.file);

        // axios
        //   .post("http://127.0.0.1:5000/api/upload", formData)
        //   .then(res => console.log(res))
        //   .catch(err => console.warn(err));

        openPopup()
    }

    const handleSubmit =()=>{
        const formData = new FormData();
        let URL = '' ;
        if(props.file !== 'http://127.0.0.1:5000/generate/anshuman.pdf'){
            formData.append("file", props.file);
            URL = "http://127.0.0.1:5000/api/upload"
        }
        else {
            URL = "http://127.0.0.1:5000/api/uploadformText"
        }

        
        formData.append("language",language);
        formData.append("speed",speed)

        const config = {     
            headers: { 'content-type': 'multipart/form-data' }
        }

        console.log(formData)
        closePopup();
        setLoader(true)
        axios
          .post(URL, formData, config)
          .then(res => {
              console.log(res);
             setLoader(false)
            //  props.setFileState('')
              history.push('/download')
            })
          .catch(err => console.warn(err));

    }

    const closePopup = ()=>{
        setShowPopUp(false);

    }
    const openPopup = ()=>{
        setShowPopUp(true);
    }

    return (
        <div>
        <div className='convertToVideoContianer'>
            <MyDocument file={props.file}/>
            <button onClick={(e)=>{onClickHandler(e)}} className='convertToVideoContainer__btn'>Convert To Video</button>
            {showPopUp?<Popup handleSpeedChange={handleSpeedChange} handleLanguageChange={handleLanguageChange} handleSubmit={handleSubmit} closePopup={closePopup}/>:null}
            {loader?<LoaderCustom/>:null}
            </div>
            <footer>
        <hr/>
        <div classname='copyright'>
    <h1>Developers</h1>
    <h2 className="names"><a href="https://github.com/IshaanDesai45">Ishaan Desai</a> </h2>
    <h2 className="names"><a href="https://github.com/sameersahu473">Sameer Ranjan Sahu </a></h2>
    <h2 className="names"><a href="https://github.com/anshusandhi6"> Anshuman Sandhibigraha</a></h2>
    <hr />
  </div>
</footer>
        </div>
    )
}

export default ConvertToVideoPage
