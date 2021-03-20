import React, { useState ,useEffect} from 'react';
import { Document, Page,pdfjs } from 'react-pdf';
import './MyDocument.css'
function MyDocument(props) {
    pdfjs.GlobalWorkerOptions.workerSrc =  
    `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`; 
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }


  return (
    <div className='pdfPreview'>
        <div className='pdfPreview__Container'>
            <Document
            file={props.file}
            onLoadSuccess={onDocumentLoadSuccess}
            >
                <Page pageNumber={pageNumber} />
            </Document>
        </div>
    </div>
  );
}

export default MyDocument

