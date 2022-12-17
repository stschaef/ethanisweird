import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  /* Display number of likes a like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      num_likes: 0,
      logname_likes_this: false
    };
    this.handleClick = this.handleClick.bind(this);
  }

  componentDidMount() {
    // Call REST API to get number of likes
    fetch(this.props.url, { credentials: 'same-origin' })
    .then((response) => {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    })
    .then((data) => {
      this.setState({
        num_likes: data.likes_count,
        logname_likes_this: data.logname_likes_this,
      });
    })
    .catch(error => console.log(error));  // eslint-disable-line no-console
  }

  handleClick(event) {
    event.preventDefault();
    // This is in the event of an unlike
    if (this.state.logname_likes_this) {
      fetch(this.props.url, {
        method: 'DELETE',
        headers: {
          'Accept': 'application/json, text/plain, */*',
          'Content-Type': 'application/json'
        }
      }).then(response => {
        if (response.status >= 200 && response.status < 300) {
            this.componentDidMount();
            this.setState({logname_likes_this : false});
            return response;
            console.log(response);
          } else {
          console.log('Somthing happened wrong');
          }
      }).catch(err => err);
    }
    // This is in the event of a like
    else {
      fetch(this.props.url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json, text/plain, */*',
          'Content-Type': 'application/json'
        }
      }).then(response => {
        if (response.status >= 200 && response.status < 300) {
            this.componentDidMount();
            this.setState({logname_likes_this : true});
            return response;
            console.log(response);
          } else {
          console.log('Somthing happened wrong');
          }
      }).catch(err => err);
   }
  }

  render() {
    // Render number of likes
    return (
      <div className="likes">
        <p>{this.state.num_likes} like{this.state.num_likes !== 1 ? 's' : ''}</p>
        <button id="like-unlike-button" onClick={this.handleClick}>
          {this.state.logname_likes_this ? 'unlike' : 'like'}
        </button>
      </div>
    );
  }
}

Likes.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Likes;
