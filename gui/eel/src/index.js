import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
//import registerServiceWorker from './service-worker__';
//import * as serviceWorker from './service-worker_ext';

import * as serviceWorker from './service-worker_ext.ts';
ReactDOM.render(<App />, document.getElementById('root'));
//registerServiceWorker();
 serviceWorker.register()