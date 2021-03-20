import React,{useState} from 'react'
import './HomePage.css'
import {history} from '../../helpers/history'
import axios from 'axios'
function HomePage(props) {

    const [text,setText] = useState('');

    const onClickHandler = (e)=>{
        e.preventDefault();

        const config = {
            headers:{
                "Content-Type" : "application/json"
            }
        }
    
        const body = JSON.stringify({text})
        props.setFileState('');
        axios.post('http://127.0.0.1:5000/convertTextToPdf',body,config)
            .then(res =>{
                console.log(res.data);
                props.setFileState('http://127.0.0.1:5000/generate/anshuman.pdf');
                history.push('/pdf_to_video');
            })
            .catch(err =>{
                console.log(err)
            })
    }

    const onChangeHandler = (e)=>{
        console.log(e.target.files[0]);
        props.setFileState(e.target.files[0]);
        history.push('/pdf_to_video');
    }

    console.log(text)

    return (
        <div>
        <div className="homePageContainer">
            <h1 >Convert Your Text in English into Interactive Visual Content</h1>
            <p>Make videos from documents and pdfs with incredible accuracy</p>
            <p>Powered by <span style={{color:"red"}}>Pi-Thons</span></p>
            <label className="homePageContainer__customFileUpload">
                <input accept="application/pdf, application/vnd.ms-excel,.txt" onChange={(e)=>{onChangeHandler(e)}}  type="file"/>
                Select PDF file
            </label>
            <h1>OR</h1>
            <div className="ui-input-container">
            <h2>Enter Your text here also to convert it in visual content</h2>
            <label className="ui-form-input-container">
                <textarea onChange={(e)=>{setText(e.target.value)}} className="ui-form-input" id="word-count-input"></textarea>
                <span className="form-input-label">Message</span>
            </label>
            <button className="button1" onClick={(e)=>{onClickHandler(e)}}>Submit</button>
            
            </div>
        </div>
        {/* <footer>
        <hr/>
  <div classname='copyright'>
    <h1>Developers</h1>
    <h2 className="names"><a href="https://github.com/IshaanDesai45">Ishaan Desai</a> </h2>
    <h2 className="names"><a href="https://github.com/sameersahu473">Sameer Ranjan Sahu </a></h2>
    <h2 className="names"><a href="https://github.com/anshusandhi6">Anshuman Sandhibigraha</a></h2>
    <hr />
  </div>
</footer> */}
        </div>
    )
}

export default HomePage
