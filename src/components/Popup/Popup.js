import React from 'react'
import './Popup.css'


const Popup = (props) => {
    return (
        <div className='popupOverlay'>
            <div className='popupOverlay__container'>
                <span>&times;</span>
                <label>
                    Language :
                    <select onChange={(e)=>{props.handleLanguageChange(e)}}>
                        <option>Hindi</option>
                        <option>Bengali</option>
                        <option>Tamil</option>
                        <option>Marathi</option>
                        <option>English</option>
                        <option>Urdu</option>
                        <option>Kannada</option>
                    </select>

                </label>
                
                <label>
                    Playback Speed :
                    <select onChange={(e)=>{props.handleSpeedChange(e)}}>
                        <option>1</option>
                        <option>0.75</option>
                        <option>0.5</option>
                        <option>0.25</option>
                        <option>1.25</option>
                        <option>1.5</option>
                    </select>
                </label>
                <button onClick={(e)=>{props.handleSubmit()}} className="popupOverlay__container__btn">
                    Submit
                </button>
            </div>
        </div>
    )
}

export default Popup
