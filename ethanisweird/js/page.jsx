import React from 'react';
import PropTypes from 'prop-types';
import Post from './post'
import InfiniteScroll from 'react-infinite-scroll-component';

// TO DO: Will want to call post in this file as well as implement infinite scrolls

class Page extends React.Component {
  /* Display page of posts
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  /*Example
    {
        "next": "",
        "results": [
        {
            "postid": 3,
            "url": "/api/v1/p/3/"
        },
        {
            "postid": 2,
            "url": "/api/v1/p/2/"
        },
        {
            "postid": 1,
            "url": "/api/v1/p/1/"
        }
        ],
        "url": "/api/v1/p/"
    }

    Another Example
    {
    "next": "/api/v1/p/?size=1&page=1",
    "results": [
        {
        "postid": 3,
        "url": "/api/v1/p/3/"
        }
    ],
    "url": "/api/v1/p/"
    }

    Return 10 newest posts by default

    ?size=N -> Return N newest posts
    ?page=N -> Return N'th page of posts  
    */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
        next_page: "",
        results_arr: [],
        flag_more: true
     };

     this.grabNext = this.grabNext.bind(this);
  }

  componentDidMount() {
    // Call REST API to get number of likes
    fetch(this.props.url, { credentials: 'same-origin' })
    .then((response) => {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    })
    .then((data) => {
      let flag_more = true;
      if (data.next === '') {
         flag_more = false;
      }
      this.setState({
        next_page: data.next,
        results_arr: data.results,
        flag_more: flag_more,
      });
    })
    .catch(error => console.log(error));  // eslint-disable-line no-console
  }

  grabNext() {
    fetch(this.state.next_page, { credentials: 'same-origin' })
    .then((response) => {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    })
    .then((data) => {
      let flag_more = true;
      if (data.next === '') {
         flag_more = false;
      }
      this.setState({
        next_page: data.next,
        results_arr: this.state.results_arr.concat(data.results),
        flag_more : flag_more
      });
    })
    .catch(error => console.log(error));  // eslint-disable-line no-console
  }

  render() {
    let posts ='';

    if( this.state.results_arr.length !== 0) {
      posts = this.state.results_arr.map((post) => 
          (
            <li key={post.postid}>
              <Post url={post.url} />
            </li>
          ));
    }

    return (
      <div className="page">
        <InfiniteScroll
          dataLength={this.state.results_arr.length} //This is important field to render the next data
          next={this.grabNext}
          hasMore={this.state.flag_more}
          loader={<h4>Loading...</h4>}
          endMessage={
            <p style={{textAlign: 'center'}}>
              <b>Yay! You have seen it all. </b>
            </p>
          }>

          {posts}

        </InfiniteScroll>
      </div>
    ) 
  }
}

Page.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Page;
