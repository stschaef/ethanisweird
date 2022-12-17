import React from 'react';
import ReactDOM from 'react-dom';
import Page from './page';
import Post from './post';

console.log("main")
ReactDOM.render(
  <Page url="/api/v1/p/" />,
  document.getElementById('reactEntry'),
);
