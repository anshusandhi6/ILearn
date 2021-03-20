import React from 'react'
import Loader from 'react-loader-spinner'
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"
import './Loader.css'
function LoaderCustom() {
    return (
        <div className="loader-overlay">
            <div className='loader-container'>
                <Loader
                    type="Bars"
                    color="rgb(255, 97, 76)"
                    height={100}
                    width={100}
                    //3 sec
                />
                <div className='loader-text'>Loading</div>
            </div>
        </div>
    )
}

export default LoaderCustom
