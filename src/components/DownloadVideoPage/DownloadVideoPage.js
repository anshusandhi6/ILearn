import React,{useState,useEffect} from 'react'
import './DownloadVideoPage.css'
import axios from 'axios'
const DownloadVideoPage = (props) => {
    let [url,setUrl] = useState('')
    let [audioUrl,setAudioUrl] = useState('')
        var x=props.file;
        console.log(props.file)


    useEffect(()=>{
        if(props.file === undefined || props.file === null || props.file.length  === 0 || props.file === "http://127.0.0.1:5000/generate/anshuman.pdf"){
            setUrl('http://127.0.0.1:5000/generate/anshuman.webm')
            setAudioUrl('http://127.0.0.1:5000/generate/anshuman.mp3')
        }
        else{
            setUrl(`http://127.0.0.1:5000/generate/${props.file.name.split('.').slice(0, -1).join('.')}.webm`)
            setAudioUrl(`http://127.0.0.1:5000/generate/${props.file.name.split('.').slice(0, -1).join('.')}.mp3`)
        }
    
    },[]);

    return (
        <div>
        <div className='DownloadVideoPageContainer'>
        <h1 className="summer">Video+Audio</h1>
            <video src={url} controls>
            </video>
            <h1 className="summer">Audio</h1>
            <div align="center">
            <audio src={audioUrl} controls>
            </audio>
            </div>

            
        </div>
        <footer>
        <hr/>
        <div classname='copyright'>
    <h1>Developers</h1>
    <h2 className="names"><a href="https://github.com/IshaanDesai45">Ishaan Desai</a> </h2>
    <h2 className="names"><a href="https://github.com/sameersahu473">Sameer Ranjan Sahu </a></h2>
    <h2 className="names"><a href="https://github.com/anshusandhi6">Anshuman Sandhibigraha</a></h2>
    <hr />
  </div>
</footer>
        </div>
        
    )
}

export default DownloadVideoPage
